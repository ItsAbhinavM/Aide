import './styles.css'
import React from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";
import App from "./App.tsx";
import { BrowserRouter } from 'react-router-dom';

console.log("Tauri frontend running");


ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <BrowserRouter >
        <App />
        </BrowserRouter>
    </React.StrictMode>
);