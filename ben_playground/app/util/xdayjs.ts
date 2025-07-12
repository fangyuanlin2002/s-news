import dayjs from "dayjs";
import timezone from "dayjs/plugin/timezone";
import utc from "dayjs/plugin/utc";

const xdayjs = dayjs;
xdayjs.extend(utc);
xdayjs.extend(timezone);

export default xdayjs;
