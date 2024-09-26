(function() {
    'use strict';

    // Fetch the healthcare tech sponsor list (supposed to be a JSON file)
    GM_xmlhttpRequest({
        method: "GET",
        url: "https://example.com/path/to/healthcare_tech_companies.json", // Replace with the actual URL of your JSON file
        onload: function(response) {
            let healthcareTechCompanies = JSON.parse(response.responseText);

            // Run the check every 5 seconds
            setInterval(function() {
                // Find the company name in the page
                let companyNameElement = document.querySelector(".job-details-jobs-unified-top-card__primary-description-container a.app-aware-link");
                if (!companyNameElement) {
                    console.log("Company name element not found");
                    return;
                }
                let companyName = companyNameElement.textContent.trim().toLowerCase();

                // Find the location in the page
                let locationAndTimeElement = companyNameElement.parentElement.textContent;
                let locationAndTime = locationAndTimeElement.split("·")[1];
                let location = locationAndTime ? locationAndTime.split("·")[0].trim() : ''; // Extracting only the location part

                // Print the company name and location
                console.log("Company name: " + companyName);
                console.log("Location: " + location);

                // Modify the healthcare tech-related terms or keywords as needed
                if (location.includes('Healthcare') || location.includes('Tech') || location.includes('Medical')) {
                    let companyLink = companyNameElement; // Save the object for the company name link

                    console.time("Matching time"); // Start timer

                    let matched = healthcareTechCompanies.sponsors.some(function(sponsor) {
                        if (isKMismatchSubstring(companyName, sponsor.toLowerCase(), 3)) {
                            // The company name is a K-mismatch substring of this company,
                            // so you can change the CSS as needed.
                            companyLink.style.fontWeight = 'bold';
                            companyLink.style.color = 'green';
                            return true;
                        }
                        return false;
                    });

                    console.timeEnd("Matching time"); // End timer and log time

                    if (!matched) {
                        // The company name did not match any sponsor,
                        // so you can change the CSS as needed.
                        console.log("Not matched!");
                        companyLink.style.fontWeight = 'bold';
                        companyLink.style.color = 'red';
                    }
                }
            }, 5000);
        }
    });
})();

function isKMismatchSubstring(query, text, k) {
    let m = query.length;
    for (let i = 0; i <= text.length - m; i++) {
        let mismatches = 0;
        for (let j = 0; j < m; j++) {
            if (text[i + j] !== query[j]) {
                mismatches++;
                if (mismatches > k) {
                    break;
                }
            }
        }
        if (mismatches <= k) {
            return true;
        }
    }
    return false;
}
