// Tải toàn bộ ảnh/font dùng trên trang chủ về thư mục local (4 request song song)
import { writeFile, mkdir } from 'node:fs/promises';
import { dirname, basename } from 'node:path';
const BASE = 'https://dulich2.themedep.top';
const U = '/wp-content/uploads/2024/03/';
const images = `user-id-svgrepo-com.svg pay-svgrepo-com.svg contact-us-svgrepo-com.svg logo-1024x818.jpg 1699857984_banner-web-vietpower1.jpg dai-loan-1.jpg du-lich-nhat-ban-tu-tuc-1-1024x684-1-1.jpg datnuochanquoc.jpg dia-diem-du-lich-thai-lan-1.jpg du-lich-phuong-hoang-co-tran-mua-nao-dep-nhat.jpg rung-tram-tra-su-ivivu.png du-lich-tay-bac-cam-nang-kinh-nghiem-cho-nguoi-lan-dau-moi-di-202202182351323122.jpg dalat3_1596178817.jpg phuquoc.jpg danang.jpg images1495076-image001_1700068315.jpg du-lich-moc-chau-tu-tuc-kinh-nghiem-cho-nguoi-moi-di-lan-dau-202202211147246504_1700126751.jpg lang-mieu-tich-thuy-du-lich-ha-khau-binh-bien-kynghidongduong-050_1699848845.jpg qiongru-193012093049-vinh-tam-a_1704270683.jpg du-lich-dai-bac-2_1693474429.jpg chi-phi-du-lich-cuu-trai-cau_1704267988.jpg mu-cang-chai-kiet-tac-ruong-bac-thang_1700122683.jpg dai-loan.jpg 8655-7e9b-4f2e-a427-18087594164f_1704267988.jpg kinh-nghiem-du-lich-thanh-do-trung-quoc-day-du-chi-tiet-nhat-5ffd498ad1d5f_1704267988.jpg Screenshot-2024-03-18-130615.png Screenshot-2024-03-18-130622.png Untitled-1-1.png ed0f76206965803bd974.jpg Thiet-ke-chua-co-ten-2023-04-04T154602.978.png photo-1678784477194-1678784477280522466320.jpg dia-diem-vui-choi-trung-thu-tiet-kiem-nhat-tu-bac-vao-nam-41.jpg sham-shui-po-thumb-800-480.jpg autumn-travel-2.jpg thanhtoan.jpg quote-open-editor-svgrepo-com.svg adobestock-274341667-1-scaled.jpeg`.split(/\s+/);
const jobs = images.map(f => [BASE + U + f, 'images/' + f]);
for (const s of [32, 180, 192]) jobs.push([`${BASE}/wp-content/uploads/2024/04/cropped-k-new-${s}x${s}.png`, `images/favicon-${s}.png`]);
for (const w of ['Regular', 'Medium', 'Bold']) for (const ext of ['woff2', 'woff'])
  jobs.push([`${BASE}/wp-content/fonts/GoogleSans/GoogleSans-${w}.${ext}`, `fonts/GoogleSans-${w}.${ext}`]);
for (const ext of ['woff2', 'woff', 'ttf'])
  jobs.push([`${BASE}/wp-content/themes/flatsome/assets/css/icons/fl-icons.${ext}?v=3.16.2`, `fonts/fl-icons.${ext}`]);

async function get([url, out]) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  await mkdir(dirname(out), { recursive: true });
  await writeFile(out, Buffer.from(await r.arrayBuffer()));
  return basename(out);
}
let ok = 0, fail = 0;
for (let i = 0; i < jobs.length; i += 4) {
  const res = await Promise.allSettled(jobs.slice(i, i + 4).map(get));
  res.forEach(r => r.status === 'fulfilled' ? ok++ : (fail++, console.error(r.reason.message)));
}
console.log(`done: ${ok} ok, ${fail} failed`);
