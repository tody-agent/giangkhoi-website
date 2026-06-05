import vi from './vi.json';
import zh from './zh.json';

const translations: Record<string, typeof vi> = { vi, zh };

export const languages = {
  vi: 'Tiếng Việt',
  zh: '中文',
};

export const defaultLang = 'vi';

export type Lang = keyof typeof languages;

/**
 * Get the current language from URL path
 */
export function getLangFromUrl(url: URL): Lang {
  const [, lang] = url.pathname.split('/');
  if (lang in languages) return lang as Lang;
  return defaultLang;
}

/**
 * Get translation function for a specific language
 */
export function useTranslations(lang: Lang) {
  return function t(key: string): string {
    const keys = key.split('.');
    let value: any = translations[lang];
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        // Fallback to default language
        value = translations[defaultLang];
        for (const fk of keys) {
          if (value && typeof value === 'object' && fk in value) {
            value = value[fk];
          } else {
            return key; // Return key if not found
          }
        }
        return value as string;
      }
    }
    
    return value as string;
  };
}

/**
 * Get path for a different language
 */
export function getLocalePath(currentPath: string, targetLang: Lang): string {
  const segments = currentPath.split('/').filter(Boolean);
  
  if (segments[0] in languages) {
    segments[0] = targetLang;
  } else {
    segments.unshift(targetLang);
  }
  
  return '/' + segments.join('/');
}

/**
 * Service slug mapping between languages
 */
export const serviceSlugMap: Record<string, Record<Lang, string>> = {
  'cuu-ho-xe-tai-lat': { vi: 'cuu-ho-xe-tai-lat', zh: 'jiu-yuan-fan-che' },
  'cau-bon-nuoc': { vi: 'cau-bon-nuoc', zh: 'diao-shui-xiang' },
  'cau-vat-lieu-xay-nha': { vi: 'cau-vat-lieu-xay-nha', zh: 'diao-jian-cai' },
  'cau-mai-ton-khung-keo': { vi: 'cau-mai-ton-khung-keo', zh: 'diao-gang-jia' },
  'cau-cay-canh': { vi: 'cau-cay-canh', zh: 'diao-jing-guan-shu' },
  'cau-may-mong-xuong': { vi: 'cau-may-mong-xuong', zh: 'diao-ji-qi' },
  'cau-container': { vi: 'cau-container', zh: 'diao-ji-zhuang-xiang' },
};

/**
 * Location slug mapping between languages
 */
export const locationSlugMap: Record<string, Record<Lang, string>> = {
  'my-hao': { vi: 'my-hao', zh: 'mi-hao' },
  'van-lam': { vi: 'van-lam', zh: 'wen-lin' },
  'yen-my': { vi: 'yen-my', zh: 'an-mei' },
  'an-thi': { vi: 'an-thi', zh: 'an-shi' },
  'van-giang': { vi: 'van-giang', zh: 'wen-jiang' },
  'khoai-chau': { vi: 'khoai-chau', zh: 'kuai-zhou' },
  'pho-noi': { vi: 'pho-noi', zh: 'phu-noi' },
  'hung-yen': { vi: 'hung-yen', zh: 'xing-an' },
};
