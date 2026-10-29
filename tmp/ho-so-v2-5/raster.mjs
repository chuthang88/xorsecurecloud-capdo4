import sharp from 'sharp';
await sharp(decodeURIComponent(new URL('03_Topo_hien_trang_kiem_ke.svg',import.meta.url).pathname),{density:180}).png().toFile(decodeURIComponent(new URL('03_Topo_hien_trang_kiem_ke.png',import.meta.url).pathname));
