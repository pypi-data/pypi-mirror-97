document.querySelector('#board_form form').onsubmit = function(){
    const form = new FormData(this);
    fetch("{{ url("/api/v0/thread") }}", {
        method: "POST",
        body: form
    }).then(res => res.json())then(res => {
        location.href = "{{ url("/") }}" + res. res._id
    });
}
