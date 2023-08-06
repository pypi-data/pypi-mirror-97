#!/usr/bin/env python

# s2p - Satellite Stereo Pipeline
# Copyright (C) 2015, Carlo de Franchis <carlo.de-franchis@polytechnique.org>
# Copyright (C) 2015, Gabriele Facciolo <facciolo@cmla.ens-cachan.fr>
# Copyright (C) 2015, Enric Meinhardt <enric.meinhardt@cmla.ens-cachan.fr>
# Copyright (C) 2015, Julien Michel <julien.michel@cnes.fr>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os.path
import json
import datetime
import multiprocessing

import numpy as np
import rasterio
from plyflatten import plyflatten_from_plyfiles_list


from s2p.config import cfg
from s2p import common
from s2p import parallel
from s2p import geographiclib
from s2p import initialization
from s2p import pointing_accuracy
from s2p import rectification
from s2p import block_matching
from s2p import masking
from s2p import triangulation
from s2p import fusion
from s2p import visualisation


def pointing_correction(tile, i):
    """
    Compute the translation that corrects the pointing error on a pair of tiles.

    Args:
        tile: dictionary containing the information needed to process the tile
        i: index of the processed pair
    """
    x, y, w, h = tile['coordinates']
    out_dir = os.path.join(tile['dir'], 'pair_{}'.format(i))
    img1 = cfg['images'][0]['img']
    rpc1 = cfg['images'][0]['rpcm']
    img2 = cfg['images'][i]['img']
    rpc2 = cfg['images'][i]['rpcm']

    # correct pointing error
    print('correcting pointing on tile {} {} pair {}...'.format(x, y, i))
    method = 'relative' if cfg['relative_sift_match_thresh'] is True else 'absolute'
    A, m = pointing_accuracy.compute_correction(
        img1, img2, rpc1, rpc2, x, y, w, h, method,
        cfg['sift_match_thresh'], cfg['max_pointing_error']
    )

    if A is not None:  # A is the correction matrix
        np.savetxt(os.path.join(out_dir, 'pointing.txt'), A, fmt='%6.3f')
    if m is not None:  # m is the list of sift matches
        np.savetxt(os.path.join(out_dir, 'sift_matches.txt'), m, fmt='%9.3f')
        np.savetxt(os.path.join(out_dir, 'center_keypts_sec.txt'),
                   np.mean(m[:, 2:], 0), fmt='%9.3f')
        if cfg['debug']:
            visualisation.plot_matches(img1, img2, rpc1, rpc2, m,
                                       os.path.join(out_dir,
                                                    'sift_matches_pointing.png'),
                                       x, y, w, h)


def global_pointing_correction(tiles):
    """
    Compute the global pointing corrections for each pair of images.

    Args:
        tiles: list of tile dictionaries
    """
    for i in range(1, len(cfg['images'])):
        out = os.path.join(cfg['out_dir'], 'global_pointing_pair_%d.txt' % i)
        l = [os.path.join(t['dir'], 'pair_%d' % i) for t in tiles]
        np.savetxt(out, pointing_accuracy.global_from_local(l),
                   fmt='%12.6f')
        if cfg['clean_intermediate']:
            for d in l:
                common.remove(os.path.join(d, 'center_keypts_sec.txt'))


def rectification_pair(tile, i):
    """
    Rectify a pair of images on a given tile.

    Args:
        tile: dictionary containing the information needed to process a tile.
        i: index of the processed pair
    """
    out_dir = os.path.join(tile['dir'], 'pair_{}'.format(i))
    x, y, w, h = tile['coordinates']
    img1 = cfg['images'][0]['img']
    rpc1 = cfg['images'][0]['rpcm']
    img2 = cfg['images'][i]['img']
    rpc2 = cfg['images'][i]['rpcm']
    pointing = os.path.join(cfg['out_dir'],
                            'global_pointing_pair_{}.txt'.format(i))

    print('rectifying tile {} {} pair {}...'.format(x, y, i))
    try:
        A = np.loadtxt(os.path.join(out_dir, 'pointing.txt'))
    except IOError:
        A = np.loadtxt(pointing)
    try:
        m = np.loadtxt(os.path.join(out_dir, 'sift_matches.txt'))
    except IOError:
        m = None

    cur_dir = os.path.join(tile['dir'],'pair_{}'.format(i))
    for n in tile['neighborhood_dirs']:
        nei_dir = os.path.join(tile['dir'], n, 'pair_{}'.format(i))
        if os.path.exists(nei_dir) and not os.path.samefile(cur_dir, nei_dir):
            sift_from_neighborhood = os.path.join(nei_dir, 'sift_matches.txt')
            try:
                m_n = np.loadtxt(sift_from_neighborhood)
                # added sifts in the ellipse of semi axes : (3*w/4, 3*h/4)
                m_n = m_n[np.where(np.linalg.norm([(m_n[:, 0] - (x + w/2)) / w,
                                                   (m_n[:, 1] - (y + h/2)) / h],
                                                  axis=0) < 3/4)]
                if m is None:
                    m = m_n
                else:
                    m = np.concatenate((m, m_n))
            except IOError:
                print('%s does not exist' % sift_from_neighborhood)

    rect1 = os.path.join(out_dir, 'rectified_ref.tif')
    rect2 = os.path.join(out_dir, 'rectified_sec.tif')
    H1, H2, disp_min, disp_max = rectification.rectify_pair(img1, img2,
                                                            rpc1, rpc2,
                                                            x, y, w, h,
                                                            rect1, rect2, A, m,
                                                            method=cfg['rectification_method'],
                                                            hmargin=cfg['horizontal_margin'],
                                                            vmargin=cfg['vertical_margin'])
    np.savetxt(os.path.join(out_dir, 'H_ref.txt'), H1, fmt='%12.6f')
    np.savetxt(os.path.join(out_dir, 'H_sec.txt'), H2, fmt='%12.6f')
    np.savetxt(os.path.join(out_dir, 'disp_min_max.txt'), [disp_min, disp_max],
                            fmt='%3.1f')

    if cfg['clean_intermediate']:
        common.remove(os.path.join(out_dir, 'pointing.txt'))
        common.remove(os.path.join(out_dir, 'sift_matches.txt'))


def stereo_matching(tile, i):
    """
    Compute the disparity of a pair of images on a given tile.

    Args:
        tile: dictionary containing the information needed to process a tile.
        i: index of the processed pair
    """
    out_dir = os.path.join(tile['dir'], 'pair_{}'.format(i))
    x, y = tile['coordinates'][:2]

    print('estimating disparity on tile {} {} pair {}...'.format(x, y, i))
    rect1 = os.path.join(out_dir, 'rectified_ref.tif')
    rect2 = os.path.join(out_dir, 'rectified_sec.tif')
    disp = os.path.join(out_dir, 'rectified_disp.tif')
    mask = os.path.join(out_dir, 'rectified_mask.png')
    disp_min, disp_max = np.loadtxt(os.path.join(out_dir, 'disp_min_max.txt'))

    block_matching.compute_disparity_map(rect1, rect2, disp, mask,
                                         cfg['matching_algorithm'], disp_min,
                                         disp_max, timeout=cfg['mgm_timeout'],
                                         max_disp_range=cfg['max_disp_range'])

    # add margin around masked pixels
    masking.erosion(mask, mask, cfg['msk_erosion'])

    if cfg['clean_intermediate']:
        if len(cfg['images']) > 2:
            common.remove(rect1)
        common.remove(rect2)
        common.remove(os.path.join(out_dir, 'disp_min_max.txt'))


def disparity_to_height(tile, i):
    """
    Compute a height map from the disparity map of a pair of image tiles.

    Args:
        tile: dictionary containing the information needed to process a tile.
        i: index of the processed pair.
    """
    out_dir = os.path.join(tile['dir'], 'pair_{}'.format(i))
    x, y, w, h = tile['coordinates']

    print('triangulating tile {} {} pair {}...'.format(x, y, i))
    rpc1 = cfg['images'][0]['rpcm']
    rpc2 = cfg['images'][i]['rpcm']
    H_ref = np.loadtxt(os.path.join(out_dir, 'H_ref.txt'))
    H_sec = np.loadtxt(os.path.join(out_dir, 'H_sec.txt'))
    disp = os.path.join(out_dir, 'rectified_disp.tif')
    mask = os.path.join(out_dir, 'rectified_mask.png')
    pointing = os.path.join(cfg['out_dir'],
                            'global_pointing_pair_{}.txt'.format(i))

    with rasterio.open(disp, 'r') as f:
        disp_img = f.read().squeeze()
    with rasterio.open(mask, 'r') as f:
        mask_rect_img = f.read().squeeze()
    height_map = triangulation.height_map(x, y, w, h, rpc1, rpc2, H_ref, H_sec,
                                          disp_img, mask_rect_img,
                                          A=np.loadtxt(pointing))

    # write height map to a file
    common.rasterio_write(os.path.join(out_dir, 'height_map.tif'), height_map)

    if cfg['clean_intermediate']:
        common.remove(H_ref)
        common.remove(H_sec)
        common.remove(disp)
        common.remove(mask)


def disparity_to_ply(tile):
    """
    Compute a point cloud from the disparity map of a pair of image tiles.

    This function is called by s2p.main only if there are two input images (not
    three).

    Args:
        tile: dictionary containing the information needed to process a tile.
    """
    out_dir = tile['dir']
    ply_file = os.path.join(out_dir, 'cloud.ply')
    plyextrema = os.path.join(out_dir, 'plyextrema.txt')
    x, y, w, h = tile['coordinates']
    rpc1 = cfg['images'][0]['rpcm']
    rpc2 = cfg['images'][1]['rpcm']

    print('triangulating tile {} {}...'.format(x, y))
    H_ref = os.path.join(out_dir, 'pair_1', 'H_ref.txt')
    H_sec = os.path.join(out_dir, 'pair_1', 'H_sec.txt')
    pointing = os.path.join(cfg['out_dir'], 'global_pointing_pair_1.txt')
    disp  = os.path.join(out_dir, 'pair_1', 'rectified_disp.tif')
    extra = os.path.join(out_dir, 'pair_1', 'rectified_disp_confidence.tif')
    if not os.path.exists(extra):    # confidence file not always generated
        extra = ''
    mask_rect = os.path.join(out_dir, 'pair_1', 'rectified_mask.png')
    mask_orig = os.path.join(out_dir, 'mask.png')

    # prepare the image needed to colorize point cloud
    colors = os.path.join(out_dir, 'rectified_ref.png')
    if cfg['images'][0]['clr']:
        hom = np.loadtxt(H_ref)
        # we want rectified_ref.png and rectified_ref.tif to have the same size
        with rasterio.open(os.path.join(out_dir, 'pair_1', 'rectified_ref.tif')) as f:
            ww, hh = f.width, f.height
        common.image_apply_homography(colors, cfg['images'][0]['clr'], hom, ww, hh)
    else:
        common.image_qauto(os.path.join(out_dir, 'pair_1', 'rectified_ref.tif'), colors)

    # compute the point cloud
    with rasterio.open(disp, 'r') as f:
        disp_img = f.read().squeeze()
    with rasterio.open(mask_rect, 'r') as f:
        mask_rect_img = f.read().squeeze()

    pyproj_out_crs = geographiclib.pyproj_crs(cfg['out_crs'])
    proj_com = "CRS {}".format(cfg['out_crs'])
    xyz_array, err = triangulation.disp_to_xyz(rpc1, rpc2,
                                               np.loadtxt(H_ref), np.loadtxt(H_sec),
                                               disp_img, mask_rect_img,
                                               pyproj_out_crs,
                                               img_bbx=(x, x+w, y, y+h),
                                               A=np.loadtxt(pointing))

    triangulation.filter_xyz_and_write_to_ply(ply_file, xyz_array,
                                              cfg['3d_filtering_r'], cfg['3d_filtering_n'],
                                              cfg['gsd'], colors, proj_com, confidence=extra)

    # compute the point cloud extrema (xmin, xmax, xmin, ymax)
    common.run("plyextrema %s %s" % (ply_file, plyextrema))

    if cfg['clean_intermediate']:
        common.remove(H_ref)
        common.remove(H_sec)
        common.remove(disp)
        common.remove(mask_rect)
        common.remove(mask_orig)
        common.remove(colors)
        common.remove(os.path.join(out_dir, 'pair_1', 'rectified_ref.tif'))


def mean_heights(tile):
    """
    """
    w, h = tile['coordinates'][2:]
    n = len(cfg['images']) - 1
    maps = np.empty((h, w, n))
    for i in range(n):
        try:
            with rasterio.open(os.path.join(tile['dir'], 'pair_{}'.format(i + 1),
                                            'height_map.tif'), 'r') as f:
                maps[:, :, i] = f.read(1)
        except RuntimeError:  # the file is not there
            maps[:, :, i] *= np.nan

    validity_mask = maps.sum(axis=2)  # sum to propagate nan values
    validity_mask += 1 - validity_mask  # 1 on valid pixels, and nan on invalid

    # save the n mean height values to a txt file in the tile directory
    np.savetxt(os.path.join(tile['dir'], 'local_mean_heights.txt'),
               [np.nanmean(validity_mask * maps[:, :, i]) for i in range(n)])


def global_mean_heights(tiles):
    """
    """
    local_mean_heights = [np.loadtxt(os.path.join(t['dir'], 'local_mean_heights.txt'))
                          for t in tiles]
    global_mean_heights = np.nanmean(local_mean_heights, axis=0)
    for i in range(len(cfg['images']) - 1):
        np.savetxt(os.path.join(cfg['out_dir'],
                                'global_mean_height_pair_{}.txt'.format(i+1)),
                   [global_mean_heights[i]])


def heights_fusion(tile):
    """
    Merge the height maps computed for each image pair and generate a ply cloud.

    Args:
        tile: a dictionary that provides all you need to process a tile
    """
    tile_dir = tile['dir']
    height_maps = [os.path.join(tile_dir, 'pair_%d' % (i + 1), 'height_map.tif')
                   for i in range(len(cfg['images']) - 1)]

    # remove spurious matches
    if cfg['cargarse_basura']:
        for img in height_maps:
            common.cargarse_basura(img, img)

    # load global mean heights
    global_mean_heights = []
    for i in range(len(cfg['images']) - 1):
        x = np.loadtxt(os.path.join(cfg['out_dir'],
                                    'global_mean_height_pair_{}.txt'.format(i+1)))
        global_mean_heights.append(x)

    # merge the height maps (applying mean offset to register)
    fusion.merge_n(os.path.join(tile_dir, 'height_map.tif'), height_maps,
                   global_mean_heights, averaging=cfg['fusion_operator'],
                   threshold=cfg['fusion_thresh'])

    if cfg['clean_intermediate']:
        for f in height_maps:
            common.remove(f)


def heights_to_ply(tile):
    """
    Generate a ply cloud.

    Args:
        tile: a dictionary that provides all you need to process a tile
    """
    # merge the n-1 height maps of the tile (n = nb of images)
    heights_fusion(tile)

    # compute a ply from the merged height map
    out_dir = tile['dir']
    x, y, w, h = tile['coordinates']
    plyfile = os.path.join(out_dir, 'cloud.ply')
    plyextrema = os.path.join(out_dir, 'plyextrema.txt')
    height_map = os.path.join(out_dir, 'height_map.tif')

    colors = os.path.join(out_dir, 'ref.tif')
    if cfg['images'][0]['clr']:
        common.image_crop_gdal(cfg['images'][0]['clr'], x, y, w, h, colors)
    else:
        common.image_qauto(common.image_crop_gdal(cfg['images'][0]['img'], x, y,
                                                 w, h), colors)

    triangulation.height_map_to_point_cloud(plyfile, height_map,
                                            cfg['images'][0]['rpcm'], x, y, colors)

    # compute the point cloud extrema (xmin, xmax, xmin, ymax)
    common.run("plyextrema %s %s" % (plyfile, plyextrema))

    if cfg['clean_intermediate']:
        common.remove(height_map)
        common.remove(colors)
        common.remove(os.path.join(out_dir, 'mask.png'))


def plys_to_dsm(tile):
    """
    Generates DSM from plyfiles (cloud.ply)

    Args:
        tile: a dictionary that provides all you need to process a tile
    """
    out_dsm  = os.path.join(tile['dir'], 'dsm.tif')
    out_conf = os.path.join(tile['dir'], 'confidence.tif')
    r = cfg['dsm_resolution']
    xmin, xmax, ymin, ymax = np.loadtxt(os.path.join(tile['dir'],
                                                     "plyextrema.txt"))

    if not all(np.isfinite([xmin, xmax, ymin, ymax])):  # then the ply is empty
        return

    # compute xoff, yoff, xsize, ysize on a grid of unit r
    xoff = np.floor(xmin / r) * r
    xsize = int(1 + np.floor((xmax - xoff) / r))

    yoff = np.ceil(ymax / r) * r
    ysize = int(1 - np.floor((ymin - yoff) / r))

    roi = xoff, yoff, xsize, ysize

    clouds = [os.path.join(tile['dir'], n_dir, 'cloud.ply') for n_dir in tile['neighborhood_dirs']]
    raster, profile = plyflatten_from_plyfiles_list(clouds,
                                                    resolution=r,
                                                    roi=roi,
                                                    radius=cfg['dsm_radius'],
                                                    sigma=cfg['dsm_sigma'])

    # save output image with utm georeferencing
    common.rasterio_write(out_dsm, raster[:, :, 0], profile=profile)

    # export confidence (optional)
    # note that the plys are assumed to contain the fields:
    # [x(float32), y(float32), z(float32), r(uint8), g(uint8), b(uint8), confidence(optional, float32)]
    # so the raster has 4 or 5 columns: [z, r, g, b, confidence (optional)]
    if raster.shape[-1] == 5:
        common.rasterio_write(out_conf, raster[:, :, 4], profile=profile)


def global_dsm(tiles):
    """
    """
    out_dsm_vrt = os.path.join(cfg['out_dir'], 'dsm.vrt')
    out_dsm_tif = os.path.join(cfg['out_dir'], 'dsm.tif')

    dsms_list = [os.path.join(t['dir'], 'dsm.tif') for t in tiles]
    dsms = '\n'.join(d for d in dsms_list if os.path.exists(d))

    input_file_list = os.path.join(cfg['out_dir'], 'gdalbuildvrt_input_file_list.txt')

    with open(input_file_list, 'w') as f:
        f.write(dsms)

    common.run("gdalbuildvrt -vrtnodata nan -input_file_list %s %s" % (input_file_list,
                                                                       out_dsm_vrt))

    res = cfg['dsm_resolution']

    if 'roi_geojson' in cfg:
        ll_poly = geographiclib.read_lon_lat_poly_from_geojson(cfg['roi_geojson'])
        pyproj_crs = geographiclib.pyproj_crs(cfg['out_crs'])
        bbx = geographiclib.crs_bbx(ll_poly, pyproj_crs)
        xoff = bbx[0]
        yoff = bbx[3]
        xsize = int(np.ceil((bbx[1]-bbx[0]) / res))
        ysize = int(np.ceil((bbx[3]-bbx[2]) / res))
        projwin = "-projwin {} {} {} {}".format(xoff, yoff,
                                                xoff + xsize * res,
                                                yoff - ysize * res)
    else:
        projwin = ""

    common.run(" ".join(["gdal_translate",
                         "-co", "TILED=YES",
                         "-co", "COMPRESS=DEFLATE",
                         "-co", "PREDICTOR=2",
                         "-co", "BIGTIFF=IF_SAFER",
                         projwin, out_dsm_vrt, out_dsm_tif]))

    # EXPORT CONFIDENCE
    out_conf_vrt = os.path.join(cfg['out_dir'], 'confidence.vrt')
    out_conf_tif = os.path.join(cfg['out_dir'], 'confidence.tif')

    dsms_list = [os.path.join(t['dir'], 'confidence.tif') for t in tiles]
    dems_list_ok = [d for d in dsms_list if os.path.exists(d)]
    dsms = '\n'.join(dems_list_ok)

    input_file_list = os.path.join(cfg['out_dir'], 'gdalbuildvrt_input_file_list2.txt')

    if len(dems_list_ok) > 0:

        with open(input_file_list, 'w') as f:
            f.write(dsms)

        common.run("gdalbuildvrt -vrtnodata nan -input_file_list %s %s" % (input_file_list,
                                                                           out_conf_vrt))

        common.run(" ".join(["gdal_translate",
                             "-co TILED=YES -co BIGTIFF=IF_SAFER",
                             "%s %s %s" % (projwin, out_conf_vrt, out_conf_tif)]))


def main(user_cfg):
    """
    Launch the s2p pipeline with the parameters given in a json file.

    Args:
        user_cfg: user config dictionary
    """
    common.print_elapsed_time.t0 = datetime.datetime.now()
    initialization.build_cfg(user_cfg)
    initialization.make_dirs()

    # multiprocessing setup
    nb_workers = multiprocessing.cpu_count()  # nb of available cores
    if cfg['max_processes'] is not None:
        nb_workers = cfg['max_processes']

    tw, th = initialization.adjust_tile_size()
    tiles_txt = os.path.join(cfg['out_dir'], 'tiles.txt')
    tiles = initialization.tiles_full_info(tw, th, tiles_txt, create_masks=True)
    if not tiles:
        print('ERROR: the ROI is not seen in two images or is totally masked.')
        sys.exit(1)

    # initialisation: write the list of tilewise json files to outdir/tiles.txt
    with open(tiles_txt, 'w') as f:
        for t in tiles:
            print(t['json'], file=f)

    n = len(cfg['images'])
    tiles_pairs = [(t, i) for i in range(1, n) for t in tiles]
    timeout = cfg['timeout']

    # local-pointing step:
    print('correcting pointing locally...')
    parallel.launch_calls(pointing_correction, tiles_pairs, nb_workers,
                          timeout=timeout)

    # global-pointing step:
    print('correcting pointing globally...')
    global_pointing_correction(tiles)
    common.print_elapsed_time()

    # rectification step:
    print('rectifying tiles...')
    parallel.launch_calls(rectification_pair, tiles_pairs, nb_workers,
                          timeout=timeout)

    # matching step:
    print('running stereo matching...')
    if cfg['max_processes_stereo_matching'] is not None:
        nb_workers_stereo = cfg['max_processes_stereo_matching']
    else:
        nb_workers_stereo = nb_workers
    parallel.launch_calls(stereo_matching, tiles_pairs, nb_workers_stereo,
                          timeout=timeout)

    if n > 2:
        # disparity-to-height step:
        print('computing height maps...')
        parallel.launch_calls(disparity_to_height, tiles_pairs, nb_workers,
                              timeout=timeout)

        print('computing local pairwise height offsets...')
        parallel.launch_calls(mean_heights, tiles, nb_workers, timeout=timeout)

        # global-mean-heights step:
        print('computing global pairwise height offsets...')
        global_mean_heights(tiles)

        # heights-to-ply step:
        print('merging height maps and computing point clouds...')
        parallel.launch_calls(heights_to_ply, tiles, nb_workers,
                              timeout=timeout)
    else:
        # triangulation step:
        print('triangulating tiles...')
        parallel.launch_calls(disparity_to_ply, tiles, nb_workers,
                              timeout=timeout)

    # local-dsm-rasterization step:
    print('computing DSM by tile...')
    parallel.launch_calls(plys_to_dsm, tiles, nb_workers, timeout=timeout)

    # global-dsm-rasterization step:
    print('computing global DSM...')
    global_dsm(tiles)
    common.print_elapsed_time()

    # cleanup
    common.garbage_cleanup()
    common.print_elapsed_time(since_first_call=True)


def make_path_relative_to_file(path, f):
    return os.path.join(os.path.abspath(os.path.dirname(f)), path)


def read_tiles(tiles_file):
    tiles = []
    outdir = os.path.dirname(tiles_file)

    with open(tiles_file) as f:
        tiles = f.readlines()

    # Strip trailing \n
    tiles = list(map(str.strip,tiles))
    tiles = [os.path.join(outdir, t) for t in tiles]

    return tiles


def read_config_file(config_file):
    """
    Read a json configuration file and interpret relative paths.

    If any input or output path is a relative path, it is interpreted as
    relative to the config_file location (and not relative to the current
    working directory). Absolute paths are left unchanged.
    """
    with open(config_file, 'r') as f:
        user_cfg = json.load(f)

    # output paths
    if not os.path.isabs(user_cfg['out_dir']):
        user_cfg['out_dir'] = make_path_relative_to_file(user_cfg['out_dir'],
                                                         config_file)

    # ROI path
    k = "roi_geojson"
    if k in user_cfg and isinstance(user_cfg[k], str) and not os.path.isabs(user_cfg[k]):
        user_cfg[k] = make_path_relative_to_file(user_cfg[k], config_file)

    if 'exogenous_dem' in user_cfg and not os.path.isabs(user_cfg['exogenous_dem']):
        user_cfg['exogenous_dem'] = make_path_relative_to_file(user_cfg['exogenous_dem'],
                                                               config_file)

    # input paths
    for img in user_cfg['images']:
        for d in ['img', 'rpc', 'clr', 'cld', 'roi', 'wat']:
            if d in img and isinstance(img[d], str) and not os.path.isabs(img[d]):
                img[d] = make_path_relative_to_file(img[d], config_file)

    return user_cfg
