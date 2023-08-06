function delta_s(date_s) {
    var then = new Date(date_s + "+0000");
    var now = new Date;
    return Math.round((now.getTime() - then.getTime()) / 1000, 2);
}

function last_seen(date_s) {
    var d = delta_s(date_s);
    if (d < 60) {
        return d + " seconds ago";
    }
    if (d < 3600) {
        return Math.round(d / 60) + " minutes ago";
    }
    if (d < 86400) {
        return Math.round(d / 3600) + " hours ago";
    }
    return Math.round(d / 86400) + " days ago";
}

function stripApi(api_link) {
    if (api_link != null) {
        return api_link.slice(5);
    }
    return "#";
}

function onDeleteClick(evt) {
    let tag_id = evt.target.id.split('-')[1];
    let r_id = 'r'+tag_id;
    let row = document.getElementById(r_id);
    fetch('/api/tags/'+tag_id, {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'},
    }).then(resp => {
        if (resp.ok) {
            row.hidden = true;
        } else {
            alert(resp.statusText);
        }
    });
}

function shouldRender(tag) {
    let show_ibeacons = document.getElementById('showIBeacons');
    let show_smartrelay = document.getElementById('showSmartRelay');
    let show_location_anchors = document.getElementById('showLocationAnchors');
    switch (tag.tag_type) {
        case 'iBeacon':
            return show_ibeacons.checked;
        case 'SmartRelay':
            return show_smartrelay.checked;
        case 'LocationAnchor':
            return show_location_anchors.checked;
    }
    return true;
}

function hideClass(c_name, p) {
    for (let el of document.getElementsByClassName(c_name)) {
        el.hidden = p;
    }
}

function onFilterChange(evt) {
    switch (evt.target.id) {
        case 'showIBeacons':
            hideClass('iBeacon', !evt.target.checked);
            break;
        case 'showSmartRelay':
            hideClass('SmartRelay', !evt.target.checked);
            break;
        case 'showLocationAnchors':
            hideClass('LocationAnchor', !evt.target.checked);
    }
}

function setupCheckBoxFilters() {
    let boxes = document.getElementsByTagName('input');
    for (let item of boxes) {
        item.addEventListener('change', onFilterChange);
    }
}

document.addEventListener("DOMContentLoaded", function(){
  "use strict";
  setupCheckBoxFilters();
  function updateProx() {
      var t_body = document.getElementById("prox_table_body");
      fetch('/api/proximity')
          .then(response => response.json())
          .then(data => {
              t_body.innerHTML = "";
              data.forEach(tag => {
                  let new_row = t_body.insertRow(-1);
                  new_row.id = 'r' + tag.tag_id;
                  new_row.hidden = !shouldRender(tag);
                  new_row.classList.add(tag.tag_type);
                  new_row.innerHTML =
                      "<td><a class=\"button\" href=\"" + stripApi(tag.links.tag) + "\">" + tag.tag_name + "</a></td>" +
                      "<td><a class=\"button\" href=\"" + stripApi(tag.links.zone) + "\">" + tag.zone_name + "</a></td>" +
                      "<td>" + tag.distance + " m</td>" +
                      "<td>" + last_seen(tag.last_seen) + "</td>" +
                      "<td>" + "<a id=\"deleteTag-" + tag.tag_id + "\" class=\"button\" href=\"#\">x</a>" + "</td>";
                  let buttons = new_row.getElementsByTagName('a');
                  for (let button of buttons) {
                      if (button.id.startsWith('deleteTag-')) {
                          button.addEventListener('click', onDeleteClick);
                      }
                  }
              });
              const refreshTime = (Math.floor(Math.random() * 1000) + 500);
              window.setTimeout(updateProx, refreshTime);
          });
  }
  updateProx();
});
