
//global variables ----------------
let data = null; //will contain filtered data, lowest price, and price range (highest - lowest)

//---------------------------------------------------------
//js helper functions for drawing + drawing functions
//--------------------------------------
// Highlight all pieces of a country
function highlightCountry(countryId) {
  document.querySelectorAll(`#world-map path[id='${countryId}'], #world-map path[class='${countryId}']`)
    .forEach(p => p.style.fill = "#f5f4ad");
}

// resets all pieces of a country
function resetCountry(countryId) {
  document.querySelectorAll(`#world-map path[id='${countryId}'], #world-map path[class='${countryId}']`)
    .forEach(p => p.style.fill = p.dataset.originalColor || "#00000094");
}

//given a value between 0 and 1, returns a color in between two colors (documentation source: https://colorjs.io/docs/interpolation)
function intColor(s) {
  const r1 = 255, g1 = 255, b1 = 255; //white
  const r2 = 1,   g2 = 128, b2 = 1; //green a lil darkish

  const r = Math.round(r1 + (r2 - r1) * s); //interpolate red
  const g = Math.round(g1 + (g2 - g1) * s); 
  const b = Math.round(b1 + (b2 - b1) * s);

  return `rgb(${r}, ${g}, ${b})`;
}

function colorMap() {
  if (!data) return; //stops if data is null
  //extraction!!! needed for the s value in the color gradient thing
  const lowest = data.lowest
  const range = data.range

  data.filtered.forEach(entry => {
    const country = entry.country;
    const price = entry.price;
    const s = (price - lowest) / range;
    const color = intColor(s);

    //coloring
    document.querySelectorAll(`#world-map path[id='${country}'], #world-map path[class='${country}']`
      ).forEach(p => {
        p.dataset.originalColor = color; //stores the original color to reuse after hover leaves
        p.style.fill = color});
  })
}

//-------------------------------------------------------
//fetching
//-----------------------------------------------------------------

async function getData() {
  const response = await fetch("/api/stats");
  data = await response.json();
}

//-----------------------------------------------
//mouse interaction side
//-------------------------------------------------------------
document.addEventListener("DOMContentLoaded", async () => {

  await getData();
  colorMap();
  document.querySelectorAll("#world-map svg path").forEach(path => {

    const countryId = path.getAttribute("id") || path.getAttribute("class"); //countries with disconnected parts like japan don't have id or names, but instead they have classes
    const countryName = path.getAttribute("name") || path.getAttribute("class"); //this will allow coloring of all parts of a country including the disconnected parts

    path.addEventListener("mouseenter", () => {
      highlightCountry(countryId);
    });

    path.addEventListener("mouseleave", () => {
      resetCountry(countryId);
    });

    path.addEventListener("click", () => {
      console.log("Clicked:", countryName); //place holder, but returns selected country's name in dev console (ctrl shift J)
    });
  });
});