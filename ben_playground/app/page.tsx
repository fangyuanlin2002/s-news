"use client";
import React, { useRef, useState } from "react";
import { TextField, Button, Autocomplete, Container, ImageList, ImageListItem } from "@mui/material";
import Title from "./components/Title";
import newsSources from "../data/constant";
import Content from "./components/Content";
import { Timestamp } from "next/dist/server/lib/cache-handlers/types";
import timeUtil from "../app/util/timeUtil";
import ImageCarousel from "./components/ImageCarousel";
import { Article } from "../data/dto";

const NEXT_PUBLIC_BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export default () => {
    const newsUrlRef = useRef<HTMLInputElement>(null);
    const [selectedMedia, setSelectedMedia] = useState<{ label: string } | null>(null);
    const [data, setData] = useState<Article | undefined>(undefined);

    const handleStartScraping = async () => {
        const newsUrl = newsUrlRef.current?.value;
        const mediaName = selectedMedia?.label;

        if (!newsUrl || !mediaName) {
            alert("Please provide both the news URL and media name.");
            return;
        }
        try {
            console.log("BACKEND_URL:", NEXT_PUBLIC_BACKEND_URL);
            const response = await fetch(`${NEXT_PUBLIC_BACKEND_URL}/web-scraping/parse-news`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    url: newsUrl,
                    media: mediaName,
                }),
            });

            const result = await response.json();
            console.log("result:", result);
            setData(result);
        } catch (error) {
            console.error("API Error:", error);
            alert("Something went wrong while calling the API.");
        }
    };

    return (
        <Container>
            <h1>Tom's test playground</h1>

            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <Title text="News URL:" />
                <TextField inputRef={newsUrlRef} style={{ width: "80%" }} label="Enter News URL" />
            </div>

            <div style={{ display: "flex", justifyContent: "left", alignItems: "center", gap: 110, marginTop: 20 }}>
                <Title text="News Media:" />
                <Autocomplete
                    disablePortal
                    options={newsSources}
                    sx={{ width: 300 }}
                    onChange={(event, newValue) => setSelectedMedia(newValue)}
                    renderInput={(params) => <TextField {...params} label="News" />}
                />
            </div>

            <div style={{ display: "flex", width: "100%", justifyContent: "end", alignItems: "center" }}>
                <Button variant="contained" style={{ marginTop: 20 }} onClick={handleStartScraping}>
                    Start Web-Scraping
                </Button>
            </div>
            {data && (
                <div style={{ marginTop: 30 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 100 }}>
                        <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start", gap: 30, marginTop: 20 }}>
                            <Content text="Published Date:" />
                            <Content text={timeUtil.timestampToChineseDate(data?.published_at) || "none"} />
                        </div>
                        <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start", gap: 30, marginTop: 20 }}>
                            <Content text={data?.origin === "native" ? "Author(s):" : "Origin:"} />
                            {data?.origin === "native" ? (
                                <Content text={data?.authors && data?.authors.length > 0 ? data.authors.join(", ") : "Unknown author"} />
                            ) : (
                                <Content text={data?.origin} />
                            )}
                        </div>
                    </div>
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", marginTop: 20 }}>
                        {data.images && data.images.length > 0 && <ImageCarousel imageUrls={data.images} />}
                    </div>
                    <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "center", gap: 130, marginTop: 20 }}>
                        <Content text="Title:" />
                        <Content text={data?.title} />
                    </div>
                    <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start", gap: 100, marginTop: 20 }}>
                        <Content text="Content:" />
                        <Content text={data?.content} />
                    </div>
                </div>
            )}
        </Container>
    );
};
