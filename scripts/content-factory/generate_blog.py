#!/usr/bin/env python3
"""
Blog Generator — Generate MDX blog posts from keyword matrix.
Produces SEO-optimized, CRO-enhanced blog posts for Xe Cẩu Giang Khôi.
"""

import json
import os
import re
import random
from typing import Dict, List, Optional
from keyword_matrix import get_keywords


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "src", "content", "blog")


def load_config() -> Dict:
    """Load content factory configuration."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')


def get_related_services(keyword: Dict, config: Dict) -> List[str]:
    """Get related service links based on keyword category."""
    links = config["internal_links"]["service_pages"]
    category = keyword["category"]

    # Priority mapping
    service_priority = {
        "cuu-ho": [0, 6, 5],      # cứu hộ, container, máy móc
        "dan-dung": [1, 2, 3, 4], # bồn nước, vật liệu, mái tôn, cây cảnh
        "cong-nghiep": [5, 6, 0], # máy móc, container, cứu hộ
        "huong-dan": [1, 0, 5],
        "bang-gia": [0, 1, 6],
        "kien-thuc": [0, 5, 1],
        "khu-vuc": [0, 1, 5],
    }

    indices = service_priority.get(category, [0, 1, 2])
    return [links[i] for i in indices if i < len(links)]


def get_related_areas(keyword: Dict, config: Dict) -> List[str]:
    """Get related area links."""
    links = config["internal_links"]["area_pages"]
    areas = keyword.get("area", [])

    if not areas:
        return random.sample(links, min(3, len(links)))

    # Map area names to slugs
    area_slug_map = {
        "Hưng Yên": ["/vi/khu-vuc/my-hao", "/vi/khu-vuc/pho-noi", "/vi/khu-vuc/hung-yen"],
        "Hà Nội": ["/vi/khu-vuc/van-lam", "/vi/khu-vuc/van-giang"],
        "Bắc Ninh": ["/vi/khu-vuc/van-lam"],
        "Bắc Giang": ["/vi/khu-vuc/yen-my"],
        "Thái Bình": ["/vi/khu-vuc/hung-yen"],
    }

    result = []
    for area in areas[:2]:
        result.extend(area_slug_map.get(area, []))
    return list(set(result))[:4]


def generate_cro_block(config: Dict) -> str:
    """Generate CRO inline block."""
    phone = config["brand"]["phoneDisplay"]
    return f"""
> **📞 Cần xe cẩu gấp?** Gọi ngay **{phone}** — Có mặt trong **30 phút**. Báo giá rõ ràng, trả tiền SAU khi xong việc.
"""


def generate_price_table(config: Dict) -> str:
    """Generate pricing table."""
    rows = []
    for t in config["tonnage_ranges"]:
        rows.append(f"| **{t['range']}** | {t['price_shift']} | {t['use']} |")

    return f"""
## Bảng giá tham khảo

| Tải trọng | Giá/ca (8h) | Phù hợp cho |
|-----------|-------------|-------------|
{chr(10).join(rows)}

*Giá chưa bao gồm VAT, phí cầu đường. Gọi **{config['brand']['phoneDisplay']}** để nhận báo giá chính xác.*
"""


def generate_trust_block(config: Dict) -> str:
    """Generate trust/social proof block."""
    return f"""
## Tại sao chọn {config['brand']['name']}?

- ✅ **{config['brand']['experience']}** kinh nghiệm trong ngành
- ✅ **{config['brand']['fleet']}** sẵn sàng phục vụ
- ✅ Có mặt trong **{config['brand']['response_time']}**
- ✅ **Báo giá rõ ràng** — không phí ẩn
- ✅ **Trả tiền SAU** khi xong việc
- ✅ Phục vụ **{config['brand']['service_hours']}** kể cả lễ Tết
"""


def generate_cta_block(config: Dict) -> str:
    """Generate bottom CTA block."""
    phone = config["brand"]["phoneDisplay"]
    zalo = config["brand"]["zalo"]
    return f"""
## Liên hệ thuê xe cẩu ngay

**{config['brand']['name']}** — {config['brand']['company']}

- 📞 **Hotline:** [{phone}](tel:{config['brand']['phone']}) (24/7)
- 💬 **Zalo:** [Chat ngay]({zalo})
- 📍 **Địa chỉ:** {config['brand']['address']}

> **Chỉ 3 bước:** Gọi điện → Báo giá → Xe đến. Đơn giản, không giấy tờ rườm rà!
"""


def generate_faq_yaml(keyword: Dict) -> str:
    """Generate FAQ YAML for frontmatter."""
    category = keyword["category"]
    area = keyword["area"][0] if keyword["area"] else "Hưng Yên"
    title_short = keyword["title"].split("—")[0].strip()

    faqs = []

    # Base FAQs by category
    if category == "cuu-ho":
        faqs = [
            {"q": f"Gọi {title_short} mất bao lâu để có xe?", "a": f"Giang Khôi có mặt trong 30 phút tại khu vực {area}. Đội 6 xe sẵn sàng 24/7, kể cả ngày lễ Tết."},
            {"q": f"Chi phí {title_short} bao nhiêu?", "a": f"Chi phí phụ thuộc vào tải trọng xe và vị trí. Giá từ 2.800.000đ/ca. Gọi 0971 491 174 để báo giá chính xác."},
            {"q": f"Có phải đặt cọc trước không?", "a": "Không cần đặt cọc. Giang Khôi cam kết trả tiền SAU khi xong việc. Uy tín 10 năm bảo chứng."},
        ]
    elif category == "dan-dung":
        faqs = [
            {"q": f"Giá {title_short} bao nhiêu?", "a": f"Giá phụ thuộc vào khối lượng hàng và tầng cao. Tải trọng 3.5T–5T giá từ 2.800.000đ/ca. Gọi 0971 491 174 để báo giá."},
            {"q": f"Cẩu có an toàn cho công trình không?", "a": "Hoàn toàn an toàn. Giang Khôi có đội ngũ kinh nghiệm 10 năm, thiết bị kiểm định đầy đủ, bảo hiểm trách nhiệm."},
            {"q": f"Cần chuẩn bị gì trước khi cẩu?", "a": "Anh/chị cần đảm bảo mặt bằng đủ rộng cho xe cẩu, thông báo trọng lượng hàng, và xác nhận vị trí nâng hạ. Đội cẩu sẽ khảo sát trước."},
        ]
    elif category == "cong-nghiep":
        faqs = [
            {"q": f"{title_short} cần xe cẩu mấy tấn?", "a": "Tùy trọng lượng hàng. Hàng dưới 5T dùng cẩu 8T; 5-15T dùng cẩu 25T; trên 15T dùng cẩu 50-100T. Gọi 0971 491 174 để tư vấn."},
            {"q": f"Có phục vụ trong KCN không?", "a": f"Có. Giang Khôi phục vụ tất cả KCN tại {area} và khu vực lân cận. Đội xe có giấy phép vào KCN đầy đủ."},
            {"q": f"Thời gian hoàn thành bao lâu?", "a": "Thông thường 2-8 giờ tùy khối lượng công việc. Giang Khôi cam kết đúng tiến độ, phối hợp chặt chẽ với khách hàng."},
        ]
    elif category in ("huong-dan", "kien-thuc"):
        faqs = [
            {"q": "Giang Khôi có cho thuê xe cẩu tại khu vực nào?", "a": "Giang Khôi phục vụ 5 tỉnh: Hưng Yên, Hà Nội, Bắc Ninh, Bắc Giang, Thái Bình. Bán kính 30km từ Mỹ Hào."},
            {"q": "Liên hệ thuê xe cẩu bằng cách nào?", "a": "Gọi Hotline 0971 491 174 (24/7) hoặc Chat Zalo. Chỉ 3 bước: Gọi → Báo giá → Xe đến."},
            {"q": "Giá thuê xe cẩu Giang Khôi có đắt không?", "a": "Giang Khôi cam kết giá cạnh tranh nhất khu vực. Báo giá rõ ràng, không phí ẩn, trả tiền SAU khi xong việc."},
        ]
    elif category in ("bang-gia",):
        faqs = [
            {"q": "Bảng giá có bao gồm VAT không?", "a": "Giá niêm yết chưa bao gồm VAT và phí cầu đường. Gọi 0971 491 174 để nhận báo giá chính xác theo công việc cụ thể."},
            {"q": "Giá cẩu đêm và ngày lễ có khác không?", "a": "Có. Cẩu đêm (sau 22h) và ngày lễ Tết tăng 15-20% so với giá ngày thường."},
            {"q": "Có được trả sau không?", "a": "Có. Giang Khôi cam kết trả tiền SAU khi xong việc. Không cần đặt cọc trước."},
        ]
    else:
        faqs = [
            {"q": f"Giang Khôi có phục vụ tại {area} không?", "a": f"Có. Giang Khôi phục vụ toàn bộ khu vực {area}. Có mặt trong 30 phút. Gọi 0971 491 174."},
            {"q": "Đội xe Giang Khôi có bao nhiêu xe?", "a": "Giang Khôi có đội 6 xe cẩu từ 3.5T đến 100T, sẵn sàng phục vụ 24/7."},
            {"q": "Có cần đặt lịch trước không?", "a": "Không bắt buộc. Gọi ngay khi cần, đội xe sẵn sàng xuất phát. Tuy nhiên, đặt trước giúp đảm bảo xe phù hợp nhất."},
        ]

    lines = ["faq:"]
    for faq in faqs:
        q = faq["q"].replace('"', '\\"')
        a = faq["a"].replace('"', '\\"')
        lines.append(f'  - question: "{q}"')
        lines.append(f'    answer: "{a}"')

    return "\n".join(lines)


def generate_content_body(keyword: Dict, config: Dict) -> str:
    """Generate the main MDX content body based on keyword category."""
    category = keyword["category"]
    title = keyword["title"]
    primary_kw = keyword["keywords"]["primary"]
    area = keyword["area"][0] if keyword["area"] else "Hưng Yên"
    phone = config["brand"]["phoneDisplay"]

    # Get internal links
    service_links = get_related_services(keyword, config)
    area_links = get_related_areas(keyword, config)

    # Internal links markdown
    service_links_md = "\n".join([f"- [{s.split('/')[-1].replace('-', ' ').title()}]({s})" for s in service_links[:3]])
    area_links_md = "\n".join([f"- [Xe cẩu {a.split('/')[-1].replace('-', ' ').title()}]({a})" for a in area_links[:3]])

    if category == "cuu-ho":
        return _gen_emergency_content(keyword, config, service_links_md, area_links_md)
    elif category == "dan-dung":
        return _gen_residential_content(keyword, config, service_links_md, area_links_md)
    elif category == "cong-nghiep":
        return _gen_industrial_content(keyword, config, service_links_md, area_links_md)
    elif category == "bang-gia":
        return _gen_pricing_content(keyword, config, service_links_md, area_links_md)
    elif category == "huong-dan":
        return _gen_guide_content(keyword, config, service_links_md, area_links_md)
    elif category == "kien-thuc":
        return _gen_knowledge_content(keyword, config, service_links_md, area_links_md)
    elif category == "khu-vuc":
        return _gen_area_content(keyword, config, service_links_md, area_links_md)
    else:
        return _gen_generic_content(keyword, config, service_links_md, area_links_md)


def _gen_emergency_content(kw, cfg, svc_links, area_links):
    area = kw["area"][0] if kw["area"] else "Hưng Yên"
    phone = cfg["brand"]["phoneDisplay"]
    pk = kw["keywords"]["primary"]

    return f"""**{pk}** — Khi xảy ra sự cố xe tải lật, container rơi hay tai nạn giao thông tại {area}, bạn cần đội cẩu cứu hộ **có mặt nhanh, xử lý chuyên nghiệp**. {cfg['brand']['name']} cam kết có mặt trong **30 phút** với đội **6 xe cẩu** từ 3.5T đến 100T.

## Khi nào cần dịch vụ {pk}?

Dịch vụ cẩu cứu hộ khẩn cấp thường cần trong các tình huống:

- **Xe tải bị lật** trên quốc lộ, đường liên huyện, đường KCN
- **Container rơi** khỏi rơ moóc, chắn đường giao thông
- **Xe sụt lầy**, mắc kẹt tại công trường hoặc đường xấu
- **Tai nạn giao thông** cần dọn hiện trường nhanh
- **Hàng hóa đổ** từ xe tải, cần thu gom và nâng lại

{generate_cro_block(cfg)}

## Quy trình cứu hộ xe tải lật tại {area}

Đội cẩu {cfg['brand']['name']} thực hiện quy trình cứu hộ **5 bước chuyên nghiệp**:

1. **Tiếp nhận cuộc gọi** — Đường dây nóng [{phone}](tel:{cfg['brand']['phone']}) hoạt động 24/7
2. **Đánh giá tình huống** — Tư vấn qua điện thoại, chọn xe cẩu phù hợp
3. **Điều xe** — Xe cẩu xuất phát từ Mỹ Hào, có mặt trong **30 phút** tại {area}
4. **Thiết lập an toàn** — Đặt biển cảnh báo, phân luồng, kiểm tra hiện trường
5. **Cẩu và khôi phục** — Nâng xe, dọn hiện trường, bàn giao

{generate_price_table(cfg)}

{generate_trust_block(cfg)}

## Khu vực phục vụ cứu hộ tại {area}

{cfg['brand']['name']} phục vụ cứu hộ xe tải lật trên toàn bộ khu vực {area} và lân cận:

{area_links}

## Dịch vụ liên quan

{svc_links}

{generate_cta_block(cfg)}
"""


def _gen_residential_content(kw, cfg, svc_links, area_links):
    area = kw["area"][0] if kw["area"] else "Hưng Yên"
    phone = cfg["brand"]["phoneDisplay"]
    pk = kw["keywords"]["primary"]

    return f"""**{pk}** — Dịch vụ cẩu chuyên nghiệp cho nhu cầu dân dụng tại {area}. {cfg['brand']['name']} với **{cfg['brand']['experience']}** kinh nghiệm, cam kết phục vụ nhanh gọn, an toàn, giá hợp lý.

## Dịch vụ {pk} bao gồm gì?

Khi anh/chị cần cẩu hàng cho mục đích dân dụng, đội cẩu {cfg['brand']['name']} sẽ hỗ trợ:

- **Khảo sát hiện trường** miễn phí qua điện thoại hoặc tại chỗ
- **Tư vấn xe cẩu** phù hợp với khối lượng và vị trí
- **Cẩu nâng hạ** an toàn, không ảnh hưởng công trình
- **Bàn giao** đúng vị trí yêu cầu

{generate_cro_block(cfg)}

## Quy trình thực hiện

1. **Liên hệ** — Gọi [{phone}](tel:{cfg['brand']['phone']}) mô tả nhu cầu
2. **Báo giá** — Nhận báo giá rõ ràng trong 5 phút
3. **Thi công** — Xe cẩu có mặt, thực hiện an toàn
4. **Nghiệm thu** — Kiểm tra, thanh toán SAU khi xong

{generate_price_table(cfg)}

## Lưu ý khi sử dụng dịch vụ

- **Mặt bằng:** Đảm bảo đường vào đủ rộng cho xe cẩu (tối thiểu 3m)
- **Trọng lượng:** Xác định trọng lượng hàng cần cẩu để chọn xe phù hợp
- **Thời tiết:** Tránh cẩu khi mưa to, gió lớn (trên cấp 4)
- **Đường điện:** Kiểm tra đường dây điện xung quanh vị trí cẩu

{generate_trust_block(cfg)}

## Khu vực phục vụ

{area_links}

## Dịch vụ liên quan

{svc_links}

{generate_cta_block(cfg)}
"""


def _gen_industrial_content(kw, cfg, svc_links, area_links):
    area = kw["area"][0] if kw["area"] else "Hưng Yên"
    phone = cfg["brand"]["phoneDisplay"]
    pk = kw["keywords"]["primary"]

    return f"""**{pk}** — Dịch vụ cẩu hàng công nghiệp chuyên nghiệp tại {area}. {cfg['brand']['name']} phục vụ các khu công nghiệp, nhà máy, xưởng sản xuất với đội xe cẩu từ 3.5T đến **100T**.

## Dịch vụ cẩu công nghiệp tại {area}

{cfg['brand']['name']} cung cấp dịch vụ cẩu hàng cho:

- **Nâng hạ container** 20ft, 40ft tại bãi và KCN
- **Di dời máy móc** — máy CNC, máy ép, máy dập, dây chuyền sản xuất
- **Lắp đặt thiết bị** — máy biến áp, cầu trục, kết cấu thép
- **Cẩu dầm thép**, kết cấu nhà xưởng, panel tường

{generate_cro_block(cfg)}

## Ưu thế khi chọn {cfg['brand']['name']}

- **Kinh nghiệm KCN:** Đã phục vụ hàng trăm nhà máy tại Phố Nối, Quế Võ, Việt Yên
- **Giấy phép đầy đủ:** Xe có giấy phép vào KCN, giấy kiểm định
- **An toàn tuyệt đối:** Đội ngũ được đào tạo an toàn lao động chuyên nghiệp
- **Linh hoạt thời gian:** Phục vụ theo lịch nhà máy, kể cả ban đêm và cuối tuần

{generate_price_table(cfg)}

## Quy trình cẩu hàng công nghiệp

1. **Khảo sát** — Đội kỹ thuật đến khảo sát hiện trường miễn phí
2. **Lập phương án** — Chọn xe cẩu, vị trí đặt, đường nâng hạ
3. **Chuẩn bị an toàn** — Đặt biển cảnh báo, kiểm tra thiết bị
4. **Thi công** — Nâng hạ theo phương án, giám sát liên tục
5. **Bàn giao** — Đặt hàng đúng vị trí, thanh toán SAU

{generate_trust_block(cfg)}

## Khu vực phục vụ

{area_links}

## Dịch vụ liên quan

{svc_links}

{generate_cta_block(cfg)}
"""


def _gen_pricing_content(kw, cfg, svc_links, area_links):
    phone = cfg["brand"]["phoneDisplay"]
    pk = kw["keywords"]["primary"]

    return f"""**{pk}** — Bảng giá thuê xe cẩu mới nhất, cập nhật tháng 6/2026. {cfg['brand']['name']} cam kết **báo giá rõ ràng, không phí ẩn, trả tiền SAU** khi xong việc.

{generate_price_table(cfg)}

{generate_cro_block(cfg)}

## Yếu tố ảnh hưởng giá thuê xe cẩu

Giá thuê xe cẩu phụ thuộc vào nhiều yếu tố:

- **Tải trọng xe cẩu** — Xe càng lớn giá càng cao
- **Thời gian thuê** — Thuê theo ca (8h), theo giờ, hoặc theo tháng
- **Khoảng cách** — Phí di chuyển xe từ bãi đến công trường
- **Thời điểm** — Đêm, lễ Tết tăng 15-20%
- **Độ phức tạp** — Vị trí hẹp, hàng đặc biệt cần thêm thiết bị phụ trợ

## So sánh giá theo hình thức thuê

| Hình thức | Thời gian | Ưu điểm | Phù hợp |
|-----------|-----------|---------|---------|
| **Theo ca** | 8 giờ | Giá cố định, không lo phát sinh | Công việc xác định rõ |
| **Theo giờ** | 1-4 giờ | Tiết kiệm cho việc nhỏ | Cẩu bồn nước, cây cảnh |
| **Theo tháng** | 30 ngày | Giá ưu đãi nhất | KCN, công trình dài hạn |

## Cách tiết kiệm chi phí thuê xe cẩu

1. **Chuẩn bị mặt bằng sẵn** — Xe vào thi công ngay, không mất thời gian chờ
2. **Xác định trọng lượng chính xác** — Chọn đúng xe, không thuê xe quá lớn
3. **Thuê theo ca** nếu việc nhiều — Rẻ hơn thuê theo giờ
4. **Đặt lịch trước** — Tránh phụ phí gấp
5. **Gom nhiều việc** cẩu cùng lúc — Tiết kiệm phí di chuyển

{generate_trust_block(cfg)}

## Dịch vụ liên quan

{svc_links}

{generate_cta_block(cfg)}
"""


def _gen_guide_content(kw, cfg, svc_links, area_links):
    phone = cfg["brand"]["phoneDisplay"]
    pk = kw["keywords"]["primary"]

    return f"""**{pk}** — Hướng dẫn chi tiết từ đội ngũ {cfg['brand']['name']} với **{cfg['brand']['experience']}** kinh nghiệm. Những kiến thức thực tế giúp anh/chị thuê xe cẩu đúng cách, an toàn và tiết kiệm.

## Hướng dẫn chi tiết

Dưới đây là hướng dẫn từng bước, dựa trên kinh nghiệm thực tế từ hàng trăm công trình mà {cfg['brand']['name']} đã phục vụ.

### Bước 1: Xác định nhu cầu

Trước khi thuê xe cẩu, anh/chị cần xác định rõ:

- **Hàng cần cẩu là gì?** (bồn nước, máy móc, vật liệu, container...)
- **Trọng lượng bao nhiêu?** (kg hoặc tấn)
- **Cần nâng lên bao nhiêu mét?** (tầng nhà, chiều cao)
- **Vị trí cẩu ở đâu?** (trong hẻm, ngoài đường, trong KCN)

### Bước 2: Chọn xe cẩu phù hợp

| Trọng lượng hàng | Xe cẩu phù hợp | Ví dụ |
|-------------------|----------------|-------|
| Dưới 2T | 3.5T – 5T | Bồn nước, cây cảnh nhỏ |
| 2T – 8T | 8T – 10T | Container 20ft, máy nhỏ |
| 8T – 20T | 15T – 25T | Máy CNC, kết cấu thép |
| Trên 20T | 50T – 100T | Dầm cầu, thiết bị nặng |

{generate_cro_block(cfg)}

### Bước 3: Chuẩn bị mặt bằng

- Đường vào đủ rộng cho xe cẩu (tối thiểu 3m)
- Mặt đất cứng, bằng phẳng cho xe dừng
- Kiểm tra đường dây điện xung quanh
- Dọn vật cản trên đường di chuyển hàng

### Bước 4: Liên hệ và báo giá

Gọi [{phone}](tel:{cfg['brand']['phone']}) để nhận báo giá trong 5 phút. Cung cấp:
- Loại hàng và trọng lượng
- Địa chỉ công trường
- Thời gian mong muốn

{generate_trust_block(cfg)}

## Dịch vụ liên quan

{svc_links}

{generate_cta_block(cfg)}
"""


def _gen_knowledge_content(kw, cfg, svc_links, area_links):
    phone = cfg["brand"]["phoneDisplay"]
    pk = kw["keywords"]["primary"]

    return f"""**{pk}** — Kiến thức chuyên sâu từ đội ngũ {cfg['brand']['name']} với **{cfg['brand']['experience']}**. Bài viết cung cấp thông tin hữu ích, giúp anh/chị hiểu rõ hơn về ngành xe cẩu.

## Tổng quan

Bài viết này sẽ giải đáp chi tiết về **{pk}**, dựa trên kinh nghiệm thực tế và kiến thức chuyên môn trong ngành cho thuê xe cẩu tại Việt Nam.

## Chi tiết

Trong ngành vận tải cẩu hàng, việc hiểu rõ các thông số kỹ thuật và quy định an toàn là vô cùng quan trọng. Dưới đây là những thông tin mà anh/chị cần biết.

### Thông số quan trọng

- **Tải trọng nâng (Load capacity):** Khối lượng tối đa xe cẩu có thể nâng
- **Tầm với (Boom reach):** Khoảng cách xa nhất cần cẩu có thể vươn tới
- **Chiều cao nâng (Lift height):** Độ cao tối đa xe cẩu có thể nâng hàng
- **Bảng tải (Load chart):** Bảng tra cứu tải trọng theo tầm với

> ⚠️ **Lưu ý:** Tải trọng nâng GIẢM khi tầm với TĂNG. Luôn kiểm tra bảng tải trước khi cẩu.

{generate_cro_block(cfg)}

{generate_price_table(cfg)}

{generate_trust_block(cfg)}

## Dịch vụ liên quan

{svc_links}

{generate_cta_block(cfg)}
"""


def _gen_area_content(kw, cfg, svc_links, area_links):
    area = kw["area"][0] if kw["area"] else "Hưng Yên"
    phone = cfg["brand"]["phoneDisplay"]
    pk = kw["keywords"]["primary"]

    return f"""**{pk}** — Dịch vụ cho thuê xe cẩu uy tín tại khu vực này. {cfg['brand']['name']} phục vụ nhanh chóng với đội **{cfg['brand']['fleet']}**, cam kết có mặt trong **30 phút**.

## Dịch vụ xe cẩu tại khu vực

{cfg['brand']['name']} cung cấp đầy đủ dịch vụ cẩu tại khu vực:

- 🚨 **Cứu hộ khẩn cấp** — Xe tải lật, container rơi, xe sụt lầy
- 🏠 **Cẩu dân dụng** — Bồn nước, cây cảnh, vật liệu xây nhà
- 🏭 **Cẩu công nghiệp** — Container, máy móc, thiết bị nhà máy
- 🏗️ **Cẩu xây dựng** — Mái tôn, khung kèo, dầm thép, bê tông

{generate_cro_block(cfg)}

## Thời gian có mặt

Xuất phát từ đội xe tại Mỹ Hào, Hưng Yên, {cfg['brand']['name']} cam kết thời gian có mặt nhanh nhất:

| Khu vực | Thời gian | Ghi chú |
|---------|-----------|---------|
| Mỹ Hào, Phố Nối | 15 phút | Trung tâm đội xe |
| Văn Lâm, Yên Mỹ | 20 phút | Lân cận |
| Văn Giang, Ân Thi | 25 phút | |
| TP Hưng Yên, Khoái Châu | 30 phút | |
| Hà Nội (Gia Lâm, Long Biên) | 30-40 phút | |
| Bắc Ninh (Từ Sơn, Tiên Du) | 35-45 phút | |

{generate_price_table(cfg)}

{generate_trust_block(cfg)}

## Dịch vụ liên quan

{svc_links}

{generate_cta_block(cfg)}
"""


def _gen_generic_content(kw, cfg, svc_links, area_links):
    return _gen_knowledge_content(kw, cfg, svc_links, area_links)


def generate_frontmatter(keyword: Dict) -> str:
    """Generate MDX frontmatter from keyword data."""
    faq_yaml = generate_faq_yaml(keyword)

    # Handle empty arrays properly in YAML
    if keyword["tags"]:
        tags_str = "tags:\n" + "\n".join([f'  - "{t}"' for t in keyword["tags"]])
    else:
        tags_str = "tags: []"

    if keyword["area"]:
        area_str = "area:\n" + "\n".join([f'  - "{a}"' for a in keyword["area"]])
    else:
        area_str = "area: []"

    if keyword["keywords"]["secondary"]:
        secondary_str = "  secondary:\n" + "\n".join([f'    - "{s}"' for s in keyword["keywords"]["secondary"]])
    else:
        secondary_str = "  secondary: []"

    if keyword["keywords"]["lsi"]:
        lsi_str = "  lsi:\n" + "\n".join([f'    - "{l}"' for l in keyword["keywords"]["lsi"]])
    else:
        lsi_str = "  lsi: []"

    return f"""---
title: "{keyword['title']}"
description: "{keyword['description']}"
date: "2026-06-06"
category: "{keyword['category']}"
priority: "{keyword['priority']}"
{tags_str}
{area_str}
keywords:
  primary: "{keyword['keywords']['primary']}"
{secondary_str}
{lsi_str}
{faq_yaml}
author: "Giang Khôi"
---
"""


def generate_blog_post(keyword: Dict, config: Dict) -> str:
    """Generate a complete MDX blog post."""
    frontmatter = generate_frontmatter(keyword)
    content = generate_content_body(keyword, config)
    return frontmatter + "\n" + content


def save_blog_post(keyword: Dict, content: str, output_dir: str) -> str:
    """Save blog post as MDX file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{keyword['slug']}.mdx")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def generate_all(output_dir: str = None, tier: str = None) -> List[str]:
    """Generate all blog posts from keyword matrix."""
    if output_dir is None:
        output_dir = OUTPUT_DIR

    config = load_config()
    keywords = get_keywords()

    if tier:
        keywords = [k for k in keywords if k["priority"] == tier]

    generated = []
    for kw in keywords:
        content = generate_blog_post(kw, config)
        filepath = save_blog_post(kw, content, output_dir)
        generated.append(filepath)
        print(f"  ✅ [{kw['id']:3d}] {kw['slug']}")

    print(f"\n🎉 Generated {len(generated)} blog posts in {output_dir}")
    return generated


if __name__ == "__main__":
    import sys

    tier = sys.argv[1] if len(sys.argv) > 1 else None
    if tier:
        print(f"🚀 Generating blog posts for tier: {tier}")
    else:
        print("🚀 Generating ALL 100 blog posts...")

    generate_all(tier=tier)
