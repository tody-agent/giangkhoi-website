# Hướng dẫn Deploy lên Cloudflare Pages

## Chuẩn bị

### 1. Tạo tài khoản Cloudflare (miễn phí)
1. Truy cập https://dash.cloudflare.com/sign-up
2. Đăng ký tài khoản miễn phí
3. Thêm domain `xecaugiangkhoi.com` vào Cloudflare DNS

### 2. Push code lên GitHub
```bash
cd giangkhoi-website
git init
git add .
git commit -m "Initial commit: xecaugiangkhoi.com"
git remote add origin https://github.com/YOUR_USERNAME/giangkhoi-website.git
git push -u origin main
```

## Deploy

### 3. Kết nối GitHub với Cloudflare Pages
1. Vào Cloudflare Dashboard → Workers & Pages → Create application
2. Chọn tab "Pages" → Connect to Git
3. Chọn repository `giangkhoi-website`
4. Cấu hình build:
   - **Framework preset**: Astro
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Node.js version**: `22`
5. Click "Save and Deploy"

### 4. Cấu hình Custom Domain
1. Sau khi deploy thành công, vào Settings → Custom Domains
2. Add domain: `xecaugiangkhoi.com`
3. Add domain: `www.xecaugiangkhoi.com` (redirect về apex)
4. Cloudflare sẽ tự cấu hình DNS record

### 5. Cấu hình Redirects
Tạo file `public/_redirects`:
```
/ /vi 302
/www.xecaugiangkhoi.com/* https://xecaugiangkhoi.com/:splat 301
```

## Sau khi Deploy

### Kiểm tra
- [ ] Truy cập https://xecaugiangkhoi.com/vi — OK
- [ ] Truy cập https://xecaugiangkhoi.com/zh — OK
- [ ] Click-to-call hoạt động trên mobile
- [ ] Zalo link mở app Zalo
- [ ] SEO: Kiểm tra https://search.google.com/search-console
- [ ] AEO: Kiểm tra /llms.txt truy cập được

### Đăng ký Google Search Console
1. Truy cập https://search.google.com/search-console
2. Add property: `xecaugiangkhoi.com`
3. Verify bằng DNS record (Cloudflare)
4. Submit sitemap: `https://xecaugiangkhoi.com/sitemap-index.xml`
