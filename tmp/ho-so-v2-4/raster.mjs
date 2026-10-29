import sharp from 'sharp';
for(const name of ['01_Topo_tong_the_DC_DR','02_Topo_phan_vung_va_luong']) {
 await sharp(decodeURIComponent(new URL(`${name}.svg`,import.meta.url).pathname),{density:180}).png().toFile(decodeURIComponent(new URL(`${name}.png`,import.meta.url).pathname));
}
