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
    const handleStartScraping = async () => {
        try {
            console.log("BACKEND_URL:", NEXT_PUBLIC_BACKEND_URL);
            const response = await fetch(`${NEXT_PUBLIC_BACKEND_URL}/web-scraping/scrape-all-taiwanese-news`, {
                method: "post",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            const result = await response.json();
            alert(`success: ${result?.success}`);
            console.log("result:", result);
        } catch (error) {
            console.error("API Error:", error);
            alert("Something went wrong while calling the API.");
        }
    };

    return (
        <Container>
            <div style={{ display: "flex", justifyContent: "center" }}>
                <Button variant="contained" style={{ marginTop: 20 }} onClick={handleStartScraping}>
                    Scrape All Taiwanese News Articles
                </Button>
            </div>
        </Container>
    );
};
