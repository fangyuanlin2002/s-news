import { Timestamp } from "next/dist/server/lib/cache-handlers/types";

export type Article = {
    url: string;
    title: string;
    content: string;
    images: string[];
    authors: string[];
    published_at: Timestamp;
    origin: string;
};
