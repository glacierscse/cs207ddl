$(document).ready(function(){

    console.log("Ready");
    function clearResults(){
      console.log("clear")
      $("#placeholder").empty();
      $("#file-name").empty();
      $("results").empty();
    }

    $("#upload-file").change(function(event){
      console.log("Browse!");
      console.log($('#upload-file').val())
      $.ajax{


      }
      $("#ts-id").val("");
    });
/**
    $("#ts-file").change(function(event){
      console.log('ts-file')
      if($("#ts-file")[0].files['length'] !== 0){
        console.log('file uploaded')
        $("#file-name").html($("#ts-file")[0].files[0]['name']);
      }
    });
  */

    function plotSimilar(response, metadata, timeseries){
      var similar_ids = [];
      // Get similar ids
      response = response['similar_points'];
      var i;
      for(i=0;i<response.length;i++){
        similar_ids.push(response[i][1]);
      }
      // For each id, get timeseries data from SM and plot
      for(i=0;i<similar_ids.length;i++){
        $.ajax({
          url: '/timeseries/'+similar_ids[i],
          type: 'GET',
          success: function(response){
            metadata.push(response['metadata']);
            timeseries.push(response['timeseries']);
          },
          error: function(response){
            console.log("Error getting timeseries from sm");
          }
        });
      }
      $(document).ajaxStop(function(){
        console.log("Finished ALL AJAX");
        var plots = [];
        var meta_msg = ["<h3>Metadata</h3><ul>"];
        for(i=0;i<timeseries.length;i++){
          var x = timeseries[i]['time'];
          var y = timeseries[i]['value'];
          var z = x.map(function(e,i){return [e, y[i]]});
          plots.push({"label":"ID"+timeseries[i]['id'],"data":z});
        }

        for(i=0;i<metadata.length;i++){
          meta_msg.push("<li>Blarg: " + metadata[i]['blarg'] +
                        " ID: " + metadata[i]['id']+
                        " Level: " + metadata[i]['level'] +
                        " Mean: " + metadata[i]['mean'] +
                        " Standard Dev: " + metadata[i]['std'] +
                        "</li>");
        }
        meta_msg.push("</ul>")
        $("#results").html(meta_msg.join(""));
        $.plot($("#placeholder"), plots,{legend: {"show": true}});
      });
    }

    $("#display-button").click(function(event){
      console.log("click display");

      var ts_id = $("#ts-id").val();
      console.log("ts_id",ts_id);
      var metadata = [];
      var timeseries = [];

      clearResults();
      if(!ts_id){
        // Use uploaded ts data
          //console.log("no id");
          $("#results").html("Please upload a JSON file...");
          var file = $("#upload-file").val();//.files[0];

          console.log('file',file[0]);
          $.ajax({
            url: '/simquery',
            type: 'POST',
            data: {"id":ts_id},
            success: function(response){
              plotSimilar(response, metadata, timeseries);
            },
            error: function(error){
              console.log("Error GET timeseries!",error);
            }
          });
          //reader.readAsText(file


      }else{
        // Get ts data from server
        $("#results").html("Fetching data from database...");
        // Get all metadata
        $.ajax({
          url: '/timeseries/'+ts_id,
          type: 'GET',
          success: function(response){
            metadata.push(response['metadata']);
            //console.log(metadata)
            timeseries.push(response['timeseries']);
            $.ajax({
              url: '/simquery',
              type: 'GET',
              data: {"id":ts_id},
              success: function(response){
                plotSimilar(response, metadata, timeseries);
              },
              error: function(error){
                console.log("Error GET timeseries!",error);
              }
            });
          },
          error: function(error){
            console.log("Error GET timeseries!",error);
          }
        });
      }
    });
    //$("#results").html(meta_msg.join(""));
})
