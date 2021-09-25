import React, { useState } from "react";
import Toggle from "../toggle/Toggle";

export default function ThemeMode({ setTheme }) {
  const [themeState, setThemeState] = useState(false);

  const updateTheme = () => {
    setThemeState(!themeState);
    setTheme(!themeState);
  };

  return <Toggle label="Dark Mode" id="4" onClick={updateTheme} />;
}
