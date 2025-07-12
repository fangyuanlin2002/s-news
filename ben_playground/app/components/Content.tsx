import React from "react";
// testing
export default ({ text }: { text: string | undefined }) => {
    return (
        <div style={{ fontSize: 20, fontWeight: 400 }}>
            {text?.split("\n").map((line, index) => (
                <React.Fragment key={line + index}>
                    {line}
                    <br />
                </React.Fragment>
            ))}
        </div>
    );
};
