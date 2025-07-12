import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight } from "lucide-react";

function ImageCarousel({ imageUrls = [] }: { imageUrls?: string[] }) {
    const [currentIndex, setCurrentIndex] = useState(0);

    if (!imageUrls || imageUrls.length === 0) {
        return <div className="carousel">No images to display</div>;
    }

    const goToPrevious = () => {
        setCurrentIndex((prev) => (prev - 1 + imageUrls.length) % imageUrls.length);
    };

    const goToNext = () => {
        setCurrentIndex((prev) => (prev + 1) % imageUrls.length);
    };

    const goToSlide = (index: number) => {
        setCurrentIndex(index);
    };

    return (
        <div className="carousel">
            <div className="carousel-image-wrapper">
                <AnimatePresence mode="wait">
                    <motion.img
                        key={imageUrls[currentIndex]}
                        src={imageUrls[currentIndex]}
                        alt={`Slide ${currentIndex}`}
                        className="carousel-image"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.5 }}
                    />
                </AnimatePresence>
            </div>

            {imageUrls.length > 1 && (
                <div className="carousel-controls">
                    <button onClick={goToPrevious} className="carousel-button">
                        {"<"}
                    </button>
                    <button onClick={goToNext} className="carousel-button">
                        {">"}
                    </button>
                </div>
            )}

            {imageUrls.length > 1 && (
                <div className="carousel-indicators">
                    {imageUrls.map((_, index) => (
                        <span key={index} className={`carousel-dot ${index === currentIndex ? "active" : ""}`} onClick={() => goToSlide(index)}></span>
                    ))}
                </div>
            )}

            <style jsx>{`
                .carousel {
                    width: 100%;
                    max-width: 600px;
                    margin: 20px auto;
                    text-align: center;
                }

                .carousel-image-wrapper {
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    position: relative;
                }

                .carousel-image {
                    width: 100%;
                    height: auto;
                    max-height: 500px;
                    object-fit: contain;
                    border-radius: 8px;
                }

                .carousel-controls {
                    margin-top: 10px;
                }

                .carousel-button {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 4px 12px;
                    font-size: 18px;
                    cursor: pointer;
                    margin: 0 5px;
                    transition: background 0.2s;
                }

                .carousel-button:hover {
                    background-color: #eee;
                }

                .carousel-indicators {
                    margin-top: 8px;
                }

                .carousel-dot {
                    display: inline-block;
                    width: 10px;
                    height: 10px;
                    margin: 0 4px;
                    background-color: #ccc;
                    border-radius: 50%;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }

                .carousel-dot.active {
                    background-color: #333;
                }
            `}</style>
        </div>
    );
}

export default ImageCarousel;
