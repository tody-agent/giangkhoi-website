# Hướng dẫn chỉnh sửa nội dung

## Cấu trúc thư mục

```
src/
├── i18n/
│   ├── vi.json          # Tất cả text tiếng Việt
│   ├── zh.json          # Tất cả text tiếng Trung
│   └── index.ts         # Hàm dịch
├── layouts/
│   └── BaseLayout.astro # Layout chung (header, footer, CTA)
├── pages/
│   ├── index.astro      # Redirect → /vi
│   ├── vi/
│   │   ├── index.astro      # Trang chủ VN
│   │   ├── bang-gia.astro   # Bảng giá VN
│   │   ├── ve-chung-toi.astro # Giới thiệu VN
│   │   └── lien-he.astro   # Liên hệ VN
│   └── zh/
│       └── index.astro      # Trang chủ TQ
├── styles/
│   └── global.css       # Design system + tokens
public/
├── images/
│   ├── hero/            # Ảnh hero banner
│   ├── services/        # Ảnh dịch vụ
│   ├── brand/           # Logo, OG image
│   └── fleet/           # Ảnh đoàn xe (chủ nhà thay ảnh thật)
├── robots.txt
├── llms.txt             # Cho AI crawlers
└── favicon.svg
```

## Chỉnh sửa nhanh

### Thay số điện thoại
Sửa trong `src/i18n/vi.json` và `src/i18n/zh.json`:
```json
"phone": "0971491174",
"phoneDisplay": "0971 491 174",
"zalo": "https://zalo.me/0971491174"
```

### Thay ảnh dịch vụ (thay ảnh AI bằng ảnh thật)
1. Copy ảnh thật vào `public/images/services/`
2. Đặt tên file giống tên cũ (VD: `cuu-ho-xe-tai-lat.png`)
3. Hoặc đổi đường dẫn ảnh trong file `.astro` tương ứng

### Thay bảng giá
Sửa mảng `pricing` trong `src/pages/vi/index.astro` dòng ~125:
```javascript
const pricing = [
  { tonnage: '3.5T – 5T', perShift: '2.800.000 – 3.400.000đ', ... },
  // Thêm/sửa dòng ở đây
];
```

### Thêm testimonial mới
Sửa mảng `testimonials` trong file trang chủ:
```javascript
const testimonials = [
  { name: 'Anh X', role: 'Chức vụ, địa chỉ', quote: 'Nội dung đánh giá...', initial: 'X' },
];
```

## Build & Test
```bash
npm run dev      # Xem thử tại localhost:4321
npm run build    # Build sản phẩm
npm run preview  # Xem bản build
```
