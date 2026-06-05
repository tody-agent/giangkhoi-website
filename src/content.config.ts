import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(170),
    date: z.string(),
    updated: z.string().optional(),
    category: z.enum([
      'cuu-ho',
      'dan-dung',
      'cong-nghiep',
      'huong-dan',
      'bang-gia',
      'kien-thuc',
      'khu-vuc',
    ]),
    tags: z.array(z.string()).default([]),
    keywords: z.object({
      primary: z.string(),
      secondary: z.array(z.string()).default([]),
      lsi: z.array(z.string()).default([]),
    }),
    area: z.array(z.string()).default([]),
    priority: z.enum(['tier1', 'tier2', 'tier3', 'tier4']).default('tier3'),
    faq: z.array(z.object({
      question: z.string(),
      answer: z.string(),
    })).default([]),
    author: z.string().default('Giang Khôi'),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    noindex: z.boolean().default(false),
  }),
});

export const collections = { blog };
