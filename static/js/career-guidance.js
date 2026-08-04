 // Function to fetch career recommendations based on skills input
 function getRecommendations() {
    const skills = document.getElementById("skillsInput").value;
    fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skills: skills })
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsDiv = document.getElementById("recommendations");
        recommendationsDiv.innerHTML = "<h3>Recommended Careers:</h3>";
        if (data.careers && data.careers.length > 0) {
            data.careers.forEach(career => {
                recommendationsDiv.innerHTML += `<p>${career.Career}</p>`;
            });
        } else {
            recommendationsDiv.innerHTML = "<p>No career matches found.</p>";
        }
    })
    .catch(error => console.error("Error:", error));
}