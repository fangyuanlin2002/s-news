export default function RootLayout({ children }: { children: React.ReactNode }) {
    // const pathname = usePathname();
    return (
        <html lang="zh-Hant">
            <body>
                <div>
                    <main>{children}</main>
                </div>
            </body>
        </html>
    );
}
