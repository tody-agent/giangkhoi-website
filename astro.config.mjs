// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

// https://astro.build/config
export default defineConfig({
  site: 'https://vantaigiangkhoi.com',
  trailingSlash: 'never',
  
  i18n: {
    defaultLocale: 'vi',
    locales: ['vi', 'zh'],
    routing: {
      prefixDefaultLocale: true,
      redirectToDefaultLocale: false,
    },
  },
  
  integrations: [
    mdx(),
    sitemap({
      i18n: {
        defaultLocale: 'vi',
        locales: {
          vi: 'vi-VN',
          zh: 'zh-CN',
        },
      },
    }),
  ],
  
  image: {
    domains: [],
  },
  
  build: {
    inlineStylesheets: 'auto',
  },
  
  vite: {
    build: {
      cssMinify: true,
    },
  },
});
