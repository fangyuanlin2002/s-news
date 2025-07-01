"use client";
import React, { useRef, useState } from "react";
import { TextField, Button, Autocomplete, Container } from "@mui/material";
import Title from "./components/Title";
import newsSources from "../dto/constant";

export default function NewsScraper() {
    const newsUrlRef = useRef<HTMLInputElement>(null);
    const [selectedMedia, setSelectedMedia] = useState<{ label: string } | null>(null);

    const handleStartScraping = async () => {
        const newsUrl = newsUrlRef.current?.value;
        const mediaName = selectedMedia;

        if (!newsUrl || !mediaName) {
            alert("Please provide both the news URL and media name.");
            return;
        }

        try {
            const response = await fetch("/api/scrape", {
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
            console.log("API Result:", result);
            alert("Scraping started. Check console for response.");
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
        </Container>
    );
}
