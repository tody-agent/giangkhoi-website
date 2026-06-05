# Vận Tải Giang Khôi – Website Dịch Vụ Xe Cẩu Hưng Yên

Website chính thức của **Công Ty TNHH Thương Mại Dịch Vụ Vận Tải Giang Khôi Hưng Yên** (Domain: [xecaugiangkhoi.com](https://xecaugiangkhoi.com)). Website được thiết kế tối ưu hóa tốc độ tải trang cực nhanh (dưới 1.5s trên mạng 4G), chuẩn SEO Google và đặc biệt là tối ưu hóa cho các công cụ tìm kiếm bằng AI (AEO - Answer Engine Optimization).

---

## 🌟 Tổng Quan Dự Án & Bối Cảnh Doanh Nghiệp

- **Doanh nghiệp**: Công Ty TNHH Thương Mại Dịch Vụ Vận Tải Giang Khôi Hưng Yên (MST: 0901150346)
- **Người đại diện**: Vũ Văn Hùng
- **Lĩnh vực hoạt động**: Dịch vụ cho thuê xe cẩu tự hành, xe cẩu chuyên dụng từ 3.5T – 100T (Đội xe gồm 6 chiếc: 3.5T, 5T, 8T, 15T, 25T, 100T) tại Hưng Yên và các tỉnh lân cận.
- **Trụ sở & Bãi xe**: Số 2013 Nguyễn Văn Linh, Phường Bạch Sam, Thị xã Mỹ Hào, Tỉnh Hưng Yên, Việt Nam.
- **Phạm vi phục vụ chính**: Bán kính 30km (Mỹ Hào, Văn Lâm, Yên Mỹ, Ân Thi, Văn Giang, Khoái Châu, Phố Nối, TP. Hưng Yên, một phần Hải Dương, Bắc Ninh & Hà Nam).
- **USP (Điểm bán hàng độc nhất)**: *"Cần cẩu GẤP ở Hưng Yên? Có mặt trong 30 phút — Báo giá rõ ràng — Thanh toán sau khi hoàn thành công việc"*.
- **Ngôn ngữ hỗ trợ**: Tiếng Việt (Mặc định) & Tiếng Trung Quốc (Nhắm tới các doanh nghiệp FDI, chủ nhà xưởng tại các Khu công nghiệp).

---

## 🛠️ Công Nghệ Sử Dụng (Tech Stack)

- **Framework**: [Astro v6](https://astro.build/) — Lựa chọn hàng đầu cho trang web nội dung tĩnh tải cực nhanh với kỹ thuật Island Architecture và khả năng xuất HTML tĩnh tối đa.
- **Tích hợp MDX**: `@astrojs/mdx` hỗ trợ viết bài viết blog và trang dịch vụ bằng Markdown mở rộng linh hoạt.
- **Styling**: Vanilla CSS thiết kế tối ưu hóa, đảm bảo hiệu suất CSS ở mức tối đa (inline tự động, CSS Minified).
- **Tối ưu hình ảnh**: Tích hợp sẵn gói `sharp` của Astro để tự động chuyển đổi, resize hình ảnh sang định dạng WebP/AVIF nhẹ hơn 70-80% so với gốc.
- **Đa ngôn ngữ (i18n)**: Sử dụng hệ thống dịch dạng JSON tĩnh cấu trúc tinh gọn để tránh làm tăng kích thước mã JS ở client.
- **Hosting & Infrastructure**: Deploy trực tiếp lên **Cloudflare Pages** (tốc độ phân phối qua Edge CDN toàn cầu, bảo mật vượt trội, chi phí $0).
- **SEO & AEO Foundation**:
  - Tích hợp tự động `@astrojs/sitemap`.
  - robots.txt hỗ trợ đầy đủ các crawler truyền thống (Googlebot, Bingbot...) và các bot AI (GPTBot, Claude-Web, PerplexityBot...).
  - File `/llms.txt` chuẩn định dạng cho các mô hình AI phục vụ việc tra cứu và huấn luyện.
  - Tích hợp schema JSON-LD cấu trúc sâu (`LocalBusiness`, `Service`, `FAQPage`, `BreadcrumbList`).

---

## 📁 Cấu Trúc Thư Mục Dự Án

Dự án được phân chia theo cấu trúc tiêu chuẩn của Astro và tích hợp hệ thống đa ngôn ngữ:

```text
giangkhoi-website/
├── src/
│   ├── components/       # Các thành phần tái sử dụng (Header, Footer, FAQ, Testimonials)
│   ├── i18n/
│   │   ├── vi.json       # Bản dịch tiếng Việt
│   │   ├── zh.json       # Bản dịch tiếng Trung Quốc
│   │   └── index.ts      # Logic hỗ trợ dịch thuật đa ngôn ngữ
│   ├── layouts/
│   │   └── BaseLayout.astro # Layout khung bao quanh (chứa SEO meta, script tracking)
│   ├── pages/
│   │   ├── index.astro   # Trang gốc (Tự động redirect sang /vi)
│   │   ├── vi/           # Phân vùng tiếng Việt
│   │   │   ├── index.astro       # Trang chủ
│   │   │   ├── bang-gia.astro    # Bảng giá thuê xe cẩu chi tiết
│   │   │   ├── ve-chung-toi.astro# Giới thiệu doanh nghiệp
│   │   │   ├── lien-he.astro     # Trang liên hệ
│   │   │   ├── blog/             # Trang danh sách bài viết & chi tiết blog
│   │   │   │   ├── index.astro
│   │   │   │   └── [...slug].astro
│   │   │   ├── dich-vu/          # Trang các dịch vụ ngách (cứu hộ, cẩu bồn nước, máy móc...)
│   │   │   └── khu-vuc/          # Trang nhắm mục tiêu khu vực (Mỹ Hào, Văn Lâm, Yên Mỹ...)
│   │   └── zh/           # Phân vùng tiếng Trung (Chủ yếu cho khối FDI, KCN)
│   │       ├── index.astro       # 首页 (Trang chủ tiếng Trung)
│   │       ├── bao-jia.astro     # 报价 (Bảng giá tiếng Trung)
│   │       ├── guan-yu.astro     # 关于 (Giới thiệu tiếng Trung)
│   │       ├── lian-xi.astro     # 联系 (Liên hệ tiếng Trung)
│   │       ├── fu-wu/            # 服务 (Dịch vụ tiếng Trung)
│   │       └── qu-yu/            # 区域 (Khu vực tiếng Trung)
│   └── styles/
│       └── global.css    # Thiết kế hệ màu thương hiệu (Vàng cẩu #FFB800, Đen #0A0A0A)
├── public/
│   ├── images/           # Thư mục chứa tài nguyên hình ảnh thực tế (đoàn xe, dịch vụ, logo)
│   ├── llms.txt          # Định nghĩa tệp tóm tắt dữ liệu cho LLMs (ChatGPT, Claude...)
│   ├── robots.txt        # Cấu hình bot tìm kiếm và bot AI
│   └── _redirects        # Quy tắc điều hướng cho Cloudflare Pages
├── package.json          # Quản lý thư viện phụ thuộc và scripts
└── astro.config.mjs      # Cấu hình Astro, i18n routing, sitemap
```

---

## ⚡ Các Tính Năng Nổi Bật

### 1. Tối Ưu Hóa AEO (Answer Engine Optimization) & SEO
- **Schema JSON-LD tự động**: Mỗi trang web tự động xuất schema `LocalBusiness` (NAP doanh nghiệp đầy đủ), `Service` (chi tiết cẩu tự hành/chuyên dụng), `FAQPage` (câu hỏi thường gặp tương ứng dịch vụ) giúp hiển thị snippet phong phú trên SERPs.
- **AI-Discovery (`llms.txt`)**: Tệp cấu trúc theo chuẩn `llmstxt.org` mô tả nhanh thông tin doanh nghiệp, bảng giá, số điện thoại liên hệ để các AI Search Engines (như Perplexity, ChatGPT Search) có thể quét nhanh và trả lời câu hỏi của người dùng một cách chính xác nhất kèm liên kết trích dẫn.
- **Robots.txt & XML Sitemap**: Tạo sơ đồ trang web tự động bao gồm cả liên kết liên ngôn ngữ (`hreflang` ngầm định). Cho phép các bot AI thu thập dữ liệu một cách tối đa.

### 2. Thiết Kế Chuyển Đổi Cao (CRO) & Mobile-First
- Hơn 95% khách hàng thuê xe cẩu sử dụng điện thoại di động khi tìm kiếm cứu hộ hoặc dịch vụ cẩu hàng.
- Nút **Gọi Ngay** (Sticky Call CTA) và liên kết **Chat Zalo** được ghim cố định ở cạnh dưới màn hình di động, giúp khách hàng liên hệ trực tiếp chỉ với một chạm.
- Tốc độ phản hồi cực nhanh nhờ kỹ thuật Zero-JS mặc định của Astro ở client (trừ khi có tương tác).

### 3. Đa Ngôn Ngữ Việt - Trung (Bilingual VI/ZH)
- Hỗ trợ đầy đủ định tuyến tĩnh `/vi/*` và `/zh/*` cho tất cả các nội dung dịch vụ cốt lõi.
- Dịch toàn diện các thành phần tĩnh qua file ngôn ngữ `src/i18n/*.json`.

---

## 🚀 Hướng Dẫn Phát Triển Dưới Local

Đảm bảo bạn đã cài đặt Node.js phiên bản mới nhất (khuyến nghị Node v22 trở lên).

### 1. Cài đặt các thư viện phụ thuộc:
```bash
npm install
```

### 2. Khởi động môi trường phát triển (Local Server):
```bash
npm run dev
```
Trang web sẽ chạy tại địa chỉ: `http://localhost:4321`

### 3. Build mã nguồn ra bản phân phối production:
```bash
npm run build
```
Bản build tĩnh hoàn chỉnh sẽ được tạo ra tại thư mục `dist/`.

### 4. Preview trước bản build tĩnh locally:
```bash
npm run preview
```

---

## ☁️ Hướng Dẫn Triển Khai (Deploy lên Cloudflare Pages)

Dự án được cấu hình hoàn toàn tương thích để chạy trên Cloudflare Pages miễn phí.

### Cấu hình build trên Cloudflare Dashboard:
1. Tạo một ứng dụng Pages mới liên kết với repository GitHub của dự án.
2. Chọn framework preset: **Astro**.
3. Các cấu hình cơ bản:
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Node.js version**: Sử dụng biến môi trường `NODE_VERSION: 22` hoặc cài đặt mặc định theo `.node-version` (đã cấu hình Node 22).
4. Thêm tên miền tùy chỉnh (Custom Domain) trong phần cài đặt: `xecaugiangkhoi.com` và tự động kích hoạt chứng chỉ SSL miễn phí của Cloudflare.
5. File `public/_redirects` sẽ tự động xử lý chuyển hướng 302 từ trang gốc `/` sang trang ngôn ngữ mặc định `/vi`.

---

## ✍️ Hướng Dẫn Cập Nhật Nội Dung Cho Chủ Đầu Tư

Mọi chỉnh sửa cơ bản có thể thực hiện thông qua việc sửa đổi các file text tĩnh mà không cần đụng tới code hệ thống:
- **Thay số điện thoại / Hotline / Link Zalo**: Thay đổi trong file [vi.json](file:///Volumes/Data/Builder/GiangKhoi/giangkhoi-website/src/i18n/vi.json) và [zh.json](file:///Volumes/Data/Builder/GiangKhoi/giangkhoi-website/src/i18n/zh.json).
- **Thay đổi bảng giá trên trang chủ**: Chỉnh sửa mảng dữ liệu `pricing` ở phần cấu hình trang [vi/index.astro](file:///Volumes/Data/Builder/GiangKhoi/giangkhoi-website/src/pages/vi/index.astro).
- **Thay đổi hình ảnh đại diện / ảnh xe**: Chỉ cần lưu các ảnh thật (xe cẩu của công ty) vào thư mục `public/images/fleet/` hoặc `public/images/services/` đè lên file cũ hoặc cập nhật đường dẫn tương ứng.

---

*Bản quyền © 2026 thuộc về Vận Tải Giang Khôi Hưng Yên.*
