document.addEventListener("DOMContentLoaded", () => {
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

// Highlight all pieces of a country
function highlightCountry(countryId) {
  document.querySelectorAll(`#world-map path[id='${countryId}'], #world-map path[class='${countryId}']`)
    .forEach(p => p.style.fill = "#ffd27f");
}

// Reset all pieces of a country
function resetCountry(countryId) {
  document.querySelectorAll(`#world-map path[id='${countryId}'], #world-map path[class='${countryId}']`)
    .forEach(p => p.style.fill = "#ececec");
}
