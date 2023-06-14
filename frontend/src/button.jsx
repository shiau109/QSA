import React from "react";



import { createRoot } from "react-dom/client";




export default function MyApp() {
return (
    <div>
    <h2>Welcome to my app</h2>
    <MyButton />
    <div id="tik"></div>

    </div>
);
}

function MyButton() {
  return (
    <button>
      I'm a button
    </button>
  );
}


function tick() {
  console.log('Load tick')

  const container = document.getElementById("tik");
  const tik = createRoot(container);
  const element = (
    <div>
      <h1>Hello, world!</h1>
      <h2>It is {new Date().toLocaleTimeString()}.</h2>
    </div>
  );
  tik.render(element);
}
// setInterval(tick, 1000);