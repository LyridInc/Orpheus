function increaseBPM() {
    let old = document.getElementById("bpm").value
    document.getElementById("bpm").value = Number(old) + 1
}

function decreaseBPM() {
    let old = document.getElementById("bpm").value
    document.getElementById("bpm").value = Number(old) - 1
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('bpm_plus').addEventListener('click', increaseBPM);
    document.getElementById('bpm_minus').addEventListener('click', decreaseBPM);
});
