function createCard(job) {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
        <h3>${job.job || job.internship}</h3>
        <p><strong>Company:</strong> ${job.company}</p>
        <p><strong>Location:</strong> ${job.place}</p>
        <p><strong>Experience:</strong> ${job.exp}</p>
        <p><strong>Salary:</strong> ${job.salary}</p>
    `;
    return card;
}

// For future filters/search
console.log("Internsathi JS loaded");


// Search Jobs
function searchJobs() {
    const query = document.getElementById("query").value;
    const place = document.getElementById("place").value;
    const exp = document.getElementById("experience").value;

    fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, place, exp })
    })
    .then(res => res.json())
    .then(data => {
        const results = document.getElementById("results");
        results.innerHTML = "";
        data.forEach(job => results.appendChild(createCard(job)));
    });
}

// Resume Upload
const resumeForm = document.getElementById("resumeForm");
if(resumeForm){
    resumeForm.addEventListener("submit", function(e){
        e.preventDefault();
        const file = document.getElementById("resume").files[0];
        const formData = new FormData();
        formData.append("resume", file);

        fetch("/upload-resume", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
            const results = document.getElementById("resume-results");
            results.innerHTML = "";
            data.forEach(job => results.appendChild(createCard(job)));

            // Employer Job Post
const employerForm = document.getElementById("employerForm");
if(employerForm){
    employerForm.addEventListener("submit", function(e){
        e.preventDefault();
        const company = document.getElementById("company").value;
        const job = document.getElementById("job").value;
        const place = document.getElementById("place").value;
        const experience = document.getElementById("experience").value;
        const salary = document.getElementById("salary").value;
        const mca_number = document.getElementById("mca_number").value;

        fetch("/employer-post", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ company, job, place, experience, salary, mca_number })
        })
        .then(res => res.json())
        .then(data => {
            const status = document.getElementById("statusMessage");
            if(data.status === "success"){
                status.innerHTML = `<p style="color:green;">${data.message}</p>`;
            } else {
                status.innerHTML = `<p style="color:red;">${data.message}</p>`;
            }
        });
    });
}

        });
    });
}
