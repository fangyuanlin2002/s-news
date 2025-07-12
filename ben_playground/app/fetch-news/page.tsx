"use client";
import React, { useRef, useState } from "react";
import { TextField, Button, Autocomplete, Container, ImageList, ImageListItem } from "@mui/material";
import { Article } from "../../data/dto";
import Content from "../components/Content";
import timeUtil from "../util/timeUtil";
import ImageCarousel from "../components/ImageCarousel";
import Title from "../components/Title";
import newsSources from "../../data/constant";

const NEXT_PUBLIC_BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
export default () => {
    const [data, setData] = useState<Article[] | undefined>(undefined);
    const [selectedMedia, setSelectedMedia] = useState<{ label: string } | null>(null);

    const handleStartScraping = async () => {
        const mediaName = selectedMedia?.label;
        try {
            console.log("BACKEND_URL:", NEXT_PUBLIC_BACKEND_URL);
            const response = await fetch(`${NEXT_PUBLIC_BACKEND_URL}/web-scraping/fetch-news/${mediaName}`, {
                method: "post",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            const result = await response.json();
            setData(result);
            console.log("result:", result);
        } catch (error) {
            console.error("API Error:", error);
            alert("Something went wrong while calling the API.");
        }
    };

    return (
        <Container>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div>
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
                    <Button variant="contained" style={{ marginTop: 20 }} onClick={handleStartScraping}>
                        Get News Articles
                    </Button>
                </div>
                <div style={{ fontWeight: "bold" }}>News count: {data ? data.length : 0}</div>
            </div>
            {data?.map((article, key) => {
                return (
                    <div style={{ marginTop: 50 }} key={key}>
                        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", marginTop: 20 }}>
                            <Content text={article?.url} />
                        </div>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 100 }}>
                            <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start", gap: 30, marginTop: 20 }}>
                                <Content text="Published Date:" />
                                <Content text={timeUtil.timestampToChineseDate(article?.published_at) || "none"} />
                            </div>
                            <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start", gap: 30, marginTop: 20 }}>
                                <Content text={article?.origin === "native" ? "Author(s):" : "Origin:"} />
                                {article?.origin === "native" ? (
                                    <Content text={article?.authors && article?.authors.length > 0 ? article.authors.join(", ") : "Unknown author"} />
                                ) : (
                                    <Content text={article?.origin} />
                                )}
                            </div>
                        </div>
                        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", marginTop: 20 }}>
                            {article.images && article.images.length > 0 && <ImageCarousel imageUrls={article.images} />}
                        </div>
                        <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "center", gap: 130, marginTop: 20 }}>
                            <Content text="Title:" />
                            <Content text={article?.title} />
                        </div>
                        <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start", gap: 100, marginTop: 20 }}>
                            <Content text="Content:" />
                            <Content text={article?.content} />
                        </div>
                    </div>
                );
            })}
        </Container>
    );
};
