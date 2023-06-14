

import '../public/index.css'

// import { ChakraProvider } from "@chakra-ui/react";

// import Todos from "./Todos.jsx";  // new


// const helloDiv = document.createElement("div");
// helloDiv.innerHTML = "Hello from Javascript!";
// document.body.append(helloDiv);

// const sayHelloManyTimes = (times) =>
//   new Array(times).fill(1).map((_, i) => `Hello ${i + 1}`);

// const helloDiv = document.createElement("div");
// helloDiv.innerHTML = sayHelloManyTimes(10).join("<br/>");
// document.body.append(helloDiv);

// const root = document.getElementById('root');


import React from "react";
import { createRoot } from "react-dom/client";
import App from "./app.jsx";
console.log('Load Index')


const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);


