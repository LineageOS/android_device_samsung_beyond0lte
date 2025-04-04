#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/exynos9820-common',
    'hardware/samsung_slsi-linaro/exynos',
    'hardware/samsung_slsi-linaro/graphics',
    'vendor/samsung/exynos9820-common',
]

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/bin/vaultkeeperd',
        'vendor/lib64/libvkservice.so'
    ): blob_fixup()
        .binary_regex_replace(b'ro.factory.factory_binary', b'ro.vendor.factory_binary\x00'),
    'vendor/lib64/libexynoscamera3.so': blob_fixup()
        .sig_replace('8B 02 20 36', '1F 20 03 D5')
        .add_needed('libshim_camera.so')
        .binary_regex_replace(b'_ZN7android5Fence', b'_ZN7exynos55Fence'),
    (
        'vendor/lib/sensors.bio.so',
        'vendor/lib/sensors.sensorhub.so',
        'vendor/lib64/sensors.bio.so',
        'vendor/lib64/sensors.sensorhub.so',
    ): blob_fixup()
        .remove_needed('libhidltransport.so')
        .add_needed('libutils-v32.so')
        .binary_regex_replace(b'_ZN7android6Thread3runEPKcim', b'_ZN7utils326Thread3runEPKcim'),
} # fmt: skip

module = ExtractUtilsModule(
    'beyond0lte',
    'samsung',
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
    blob_fixups=blob_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'exynos9820-common', module.vendor
    )
    utils.run()
