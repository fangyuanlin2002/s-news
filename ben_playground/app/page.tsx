import Link from "next/link";
import { Input, TextField } from "@mui/material";
import React from "react";
import Image from "next/image";
import Title from "./components/Title";

export default () => {
    return (
        <div>
            <h1>Tom's test playground</h1>
            <div style={{ display: "flex", justifyContent: "left", alignItems: "center" }}>
                <Title text="News URL:" />
                <TextField slotProps={{ htmlInput: { "data-testid": "…" } }} />
            </div>
        </div>
    );
};
