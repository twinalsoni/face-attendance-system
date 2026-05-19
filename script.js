async function markAttendance(){

    const name =
        document.getElementById("name").value;

    if(name === ""){

        alert("Please Enter Name");

        return;
    }

    const response = await fetch(
        "http://127.0.0.1:5000/mark-attendance",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name
            })
        }
    );

    const data = await response.json();

    alert(data.message);

    document.getElementById("name").value = "";

    loadAttendance();
}

async function loadAttendance(){

    const response = await fetch(
        "http://127.0.0.1:5000/attendance"
    );

    const data = await response.json();

    const attendanceList =
        document.getElementById("attendanceList");

    attendanceList.innerHTML = "";

    data.forEach(item => {

        const li = document.createElement("li");

        li.innerText =
            `${item.name} - ${item.date} - ${item.time}`;

        attendanceList.appendChild(li);
    });
}

loadAttendance();