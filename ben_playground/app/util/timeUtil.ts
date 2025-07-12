function timestampToChineseDate(timestamp: number): string {
    const date = new Date(timestamp * 1000); // Convert from seconds to milliseconds

    const options: Intl.DateTimeFormatOptions = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
        weekday: "long",
    };
    console.log(date.toLocaleDateString("zh-CN", options));

    return date.toLocaleDateString("zh-CN", options);
}

function dateToStartingTimestampOfTheDay(date: string | undefined | null) {
    if (!date) return undefined;
    const parts = date.split("/");
    const month = parseInt(parts[0], 10) - 1; // month is 0-based in JS Date
    const day = parseInt(parts[1], 10);
    const year = parseInt(parts[2], 10);

    const startDate = new Date(year, month, day, 0, 0, 0);
    return Math.floor(startDate.getTime() / 1000);
}

function dateToEndingTimestampOfTheDay(date: string | undefined | null) {
    if (!date) return undefined;
    const parts = date.split("/");
    const month = parseInt(parts[0], 10) - 1;
    const day = parseInt(parts[1], 10);
    const year = parseInt(parts[2], 10);

    const endDate = new Date(year, month, day, 23, 59, 59);
    return Math.floor(endDate.getTime() / 1000);
}

export default { timestampToChineseDate, dateToStartingTimestampOfTheDay, dateToEndingTimestampOfTheDay };
