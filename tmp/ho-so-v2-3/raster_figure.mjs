import fs from 'node:fs/promises';
import sharp from 'sharp';
const dir='/Users/thangchu/Documents/ChatGPT/XOR Secure Cloud/tmp/ho-so-v2-3';
await sharp(await fs.readFile(dir+'/So_do_kien_truc_muc_tieu.svg'),{density:200}).png().toFile(dir+'/So_do_kien_truc_muc_tieu.png');
