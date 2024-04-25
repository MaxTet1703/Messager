$(function($){
    ymaps.ready(function(){
        var map = new ymaps.Map("map", {
            center: [56.0102763820674, 92.85198816311457],
            zoom: 15,
            controls: []
        });
        console.log(map.geoObjects);
        map.events.add("click", (e) => {
            map.geoObjects.removeAll();
            map.geoObjects.add(new ymaps.Placemark(e.get("coords")));
            $('input[name="latitude"]').val(e.get("coords")[1]);
            $('input[name="longitude"]').val(e.get("coords")[0]);
        })
        fetch('http://' + window.location.host + '/map_info/')
            .then(response => response.json())
            .then(data => {
                console.log(data)
                render_maps(data)
            })
            .catch(error => console.error(error))
    });
    $("#make-mem").submit(function(e){
        e.preventDefault();
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response){
                console.log(response.mes);
                window.location.reload()
            },
            error: function(xhr, status, error){
                console.log("Фиаско, братан");
                console.log(error);
            }

        });
    });
    function render_maps(data){
        Array.from(data).forEach(element => {
            var map = new ymaps.Map(`map${element.pk}`,{
                center: [element.longitude, element.latitude],
                zoom: 15,
                controls: []
            });
            map.geoObjects.add(new ymaps.Placemark([element.longitude, element.latitude])) 
        });
    }
});