"use client";
import React, { useRef, useState } from "react";
import { TextField, Button, Autocomplete, Container, ImageList, ImageListItem } from "@mui/material";
import { Article } from "../../data/dto";
import Content from "../components/Content";
import timeUtil from "../util/timeUtil";
import ImageCarousel from "../components/ImageCarousel";
import Title from "../components/Title";
import newsSources from "../../data/constant";
import { DateCalendar } from "@mui/x-date-pickers/DateCalendar";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { DatePicker } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";

const NEXT_PUBLIC_BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;
console.log("NEXT_PUBLIC_BACKEND_URL:", NEXT_PUBLIC_BACKEND_URL);
const origins = [{ label: "native" }, ...newsSources];
export default () => {
    const [data, setData] = useState<Article[] | undefined>(undefined);
    const authorRef = useRef<HTMLInputElement>(null);
    const [selectedMedia, setSelectedMedia] = useState<{ label: string } | null>(null);
    const [selectedOrigin, setSelectedOrigin] = useState<{ label: string } | null>(null);
    const dateRef = useRef<HTMLInputElement>(null);

    const handleGetDate = () => {
        const value = dateRef.current?.value;
        console.log("📅 Selected Date:", value);
        alert(`Selected Date: ${value}`);
    };

    const handleGetNews = async () => {
        console.log("media_name:", selectedMedia?.label);
        console.log("date:", dateRef.current?.value);
        console.log("selectedOrigin:", selectedOrigin?.label);
        console.log("authorRef.current?.value:", authorRef.current?.value);
        try {
            console.log("BACKEND_URL:", NEXT_PUBLIC_BACKEND_URL);
            const response = await fetch(`${NEXT_PUBLIC_BACKEND_URL}/web-scraping/get-news`, {
                method: "post",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    media_name: selectedMedia?.label,
                    start_time: timeUtil.dateToStartingTimestampOfTheDay(dateRef.current?.value),
                    end_time: timeUtil.dateToEndingTimestampOfTheDay(dateRef.current?.value),
                    origin: selectedOrigin?.label,
                    authors: authorRef.current?.value ? [authorRef.current?.value] : [],
                }),
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
            <div style={{ display: "flex", justifyContent: "center" }}>
                <div style={{ fontWeight: "bold" }}>News count: {data ? data.length : 0}</div>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", justifyContent: "left", alignItems: "center", gap: 20, marginTop: 20 }}>
                    <Title text="News Media:" />
                    <Autocomplete
                        disablePortal
                        options={newsSources}
                        sx={{ width: 300 }}
                        onChange={(event, newValue) => setSelectedMedia(newValue)}
                        renderInput={(params) => <TextField {...params} label="News" />}
                    />
                </div>
                <div style={{ display: "flex", justifyContent: "left", alignItems: "center", gap: 20, marginTop: 20 }}>
                    <Title text="Origin:" />
                    <Autocomplete
                        disablePortal
                        options={origins}
                        sx={{ width: 300 }}
                        onChange={(event, newValue) => setSelectedOrigin(newValue)}
                        renderInput={(params) => <TextField {...params} label="News" />}
                    />
                </div>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 20 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
                    <Title text="Date:" />
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <div style={{ display: "flex", flexDirection: "column", gap: 20, width: 300 }}>
                            <DatePicker
                                label="Pick Date"
                                defaultValue={new Date()}
                                slotProps={{
                                    textField: {
                                        inputRef: dateRef,
                                    },
                                }}
                            />
                        </div>
                    </LocalizationProvider>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
                    <Title text="Author:" />
                    <TextField id="outlined-basic" label="Outlined" variant="outlined" inputRef={authorRef} />
                </div>
            </div>
            <div style={{ display: "flex", justifyContent: "center" }}>
                <Button variant="contained" style={{ marginTop: 20 }} onClick={handleGetNews}>
                    Get News Articles
                </Button>
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
                        <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "flex-start", gap: 100, marginTop: 20 }}>
                            <Content text="Content in English:" />
                            <Content text={article?.content_en} />
                        </div>
                    </div>
                );
            })}
        </Container>
    );
};
