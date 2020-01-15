let saved = [];
let partiesInclQueue = [];
let partiesExclQueue = [];
let getSaved = () => saved;
let getPartiesInclQueue = () => partiesInclQueue;
let getPartiesExclQueue = () => partiesExclQueue;
let pushToSaved = (newVal) => saved.push(newVal);
let pushToPartiesInclQueue = (newVal) => partiesInclQueue.push(newVal);
let pushToPartiesExclQueue = (newVal) => partiesExclQueue.push(newVal);
let clearSaved = () => saved = [];
let clearPartiesInclQueue = () => partiesInclQueue = [];
let clearPartiesExclQueue = () => partiesExclQueue = [];
let removeFromSaved = (val) => {
  console.log("Before ", saved.length)
  if (saved.length == 1) {
    saved = [];
  } else {
    let ind = saved.indexOf(val);
    saved.splice(ind, 1);
    for (let i = 0; i < saved.length; i++) {
      console.log(saved[i])
    }
  }
  console.log("After ", saved.length)
}

$(document).ready(function() {
  renderRegions();
  renderParties();
  renderExperience();
  renderStudies();
  renderSentence();
  renderAges();
  renderGenders();
  processCandidate();
  renderUpdate();
});

function clearResultsDisplay(shouldGoToFirstPage) {
  $('#generate-here').html('<p>Cargando...</p>');
  $("#generate-currpage").html('');
  $('#generate-arrows').html('');
  $('#generate-amount').html('');
  if (shouldGoToFirstPage) goToPageN(1);
}

function reloadFilters() {
  $('#generate-filters').html('');
  renderHistory();
}

function clearSavedDisplay() {
  $("#generate-saved").html('<p>Cargando...</p>');
}

const renderCandidatesData = async () => {

  const candidatesData = await fetch('/candidatesData')
      .then(res => res.json())
      .catch(error => console.log("ERROR"));

  $('#generate-here').html('');

  if (candidatesData.length == 0) {
    $("#generate-here").append($("<p>", {text: "Ningún candidato encontrado!"}));
    return;
  }

  let $titleWrapper = $("<div>");
  let $titles = $("<div>", {"class": "row"});
  Object.keys(candidatesData[0]).filter(key => key != "H-Link").forEach(key => $titles.append(getNewCol(key.substring(2))));
  $titleWrapper.append($titles);
  let $titleHrTag = $("<hr>");
  $titleWrapper.append($titleHrTag);
  $("#generate-here").append($titleWrapper);

  for (let i = 0; i < candidatesData.length; i++) {
    let dict = candidatesData[i]

    let $newWrapper = $("<div>", {"class": "candidate"});

    let $newRow = $("<div>", {"class": "row"});

    let $firstCol = $("<div>", {"class": "col-md-1"});
    let $firstTag = $("<a>", {href: dict["H-Link"], target: "_blank", text: dict["A-Nombre"]});
    $firstCol.append($firstTag);
    $newRow.append($firstCol);
    Object.keys(dict).slice(1).filter(key => key != "H-Link").forEach(key => $newRow.append(getNewCol(dict[key])));

    $newRow.append(renderCheckbox(i));
    $newRow.append($formcheck);

    $newWrapper.append($newRow);

    let $newHrTag = $("<hr>");
    $newWrapper.append($newHrTag);

    $("#generate-here").append($newWrapper);
  }

  $('#generate-amount').html('');
  renderAmountResults();

  $("#generate-currpage").html('');
  renderCurrentPage();

  $('#generate-arrows').html('');
  renderArrows();

  $("#saveButtonContainer").html('');
  renderSave();
}

function getNewCol(val) {
  let $newCol = $("<div>", {"class": "col-md-1"});
  let $newTag = (val.substring(0,4) == "http") ? $("<img>", {src: val, height: 50, width: 50}) : $("<p>", {text: val});
  $newCol.append($newTag);
  return $newCol;
}

const renderCheckbox = (ind) => {
  $formcheck = $("<div>", {"class": "form-check col-md-1"});
  $label = $("<label>", {"class": "form-check-label"});
  $checkbox = $("<input/>", {type: "checkbox", "class": "form-check-input", id: "checkbox " + ind.toString()});
  $label.append($checkbox);
  $formcheck.append($label);
  $checkbox.change(function() {
    let check = ($(this).prop('checked'));
    console.log(check);
    if (check) {
      pushToSaved(ind);
    } else {
      removeFromSaved(ind);
    }
  });
  return $formcheck;
}

const renderRegions = async () => {
  const regions = await fetch('/regions')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));

  let $ddMRegions = $("#ddMRegions");
  regions.forEach(region => $ddMRegions.append(getNewDDIRegion(region)));
}

function getNewDDIRegion(val) {
  let $newDDI = $("<a>", {"class": "dropdown-item", href: "#", text: val});
  $newDDI.click((e) => {
    e.preventDefault();
    postRegion(val);
    reloadFilters();
  });
  return $newDDI;
}

const postRegion = async (val) => {
  fetch('/updateRegions', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const renderParties = async () => {
  const parties = await fetch('/parties')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));
  let $ddMPartiesIncl = $("#ddMPartiesIncl");
  let $ddMPartiesEcxl = $("#ddMPartiesExcl");
  parties.forEach(party => $ddMPartiesIncl.append(getNewDDIParty("incl", party)));
  parties.forEach(party => $ddMPartiesEcxl.append(getNewDDIParty("excl", party)));
  submitPartiesOnClick("#submitPartiesIncl", "/updatePartiesIncl");
  submitPartiesOnClick("#submitPartiesExcl", "/updatePartiesExcl");
}

function getNewDDIParty(type, val) {
  let $newDDI = $("<a>", {"class": "dropdown-item", href: "#", text: val});
  $newDDI.click((e) => {
    e.preventDefault();
    if (type == "incl") pushToPartiesInclQueue(val)
    if (type == "excl") pushToPartiesExclQueue(val)
    console.log("Added " + val + " to the queue!")
  })
  return $newDDI;
}

function submitPartiesOnClick(submitId, url) {
  $(submitId).click((e) => {
    e.preventDefault();
    if (submitId == "#submitPartiesIncl") postParty(url, getPartiesInclQueue());
    if (submitId == "#submitPartiesExcl") postParty(url, getPartiesExclQueue());
    reloadFilters();
  });
}

const postParty = async (url, val) => {
  fetch(url, {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}


function renderExperience() {
  $("#cbExperience").click(function() {
    let check = ($(this).prop('checked'));
    console.log(check);
    if (check) {
      postExperience();
      reloadFilters();
    } else {
      console.log("NOPE");
    }
  });
}

const postExperience = async () => {
  let val = "";
  fetch('/updateExperience', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const renderStudies = async () => {
  const studies = await fetch('/studies')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));

  let $ddMStudies = $("#ddMStudies");
  studies.forEach(studyLevel => $ddMStudies.append(getNewDDIStudyLevel(studyLevel)));
}

function getNewDDIStudyLevel(val) {
  let $newDDI = $("<a>", {"class": "dropdown-item", href: "#", text: val});
  $newDDI.click((e) => {
    e.preventDefault();
    postStudyLevel(val);
    reloadFilters();
  });
  return $newDDI;
}

const postStudyLevel = async (val) => {
  fetch('/updateStudies', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

function renderSentence() {
  $("#cbSentence").click(function() {
    let check = ($(this).prop('checked'));
    console.log(check);
    if (check) {
      postSentence();
      reloadFilters();
    } else {
      console.log("NOPE");
    }
  });
}

const postSentence = async () => {
  let val = "";
  fetch('/updateSentence', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const renderAges = async () => {
  const ages = Array(100 - 25 + 1).fill().map((_, idx) => 25 + idx);

  let $ddMAgeLower = $("#ddMAgeLower");
  let $ddMAgeUpper = $("#ddMAgeUpper");
  ages.forEach(age => $ddMAgeLower.append(getNewDDIAge("updateAgeLower", age)));
  ages.forEach(age => $ddMAgeUpper.append(getNewDDIAge("updateAgeUpper", age)));
}

function getNewDDIAge(url, val) {
  let $newDDI = $("<a>", {"class": "dropdown-item", href: "#", text: val});
  $newDDI.click((e) => {
    e.preventDefault();
    postAge(url, val);
    reloadFilters();
  });
  return $newDDI;
}

const postAge = async (url, val) => {
  fetch(url, {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const renderGenders = async () => {
  const genders = ['Hombre', 'Mujer']

  let $ddMGenders = $("#ddMGenders");
  genders.forEach(gender => $ddMGenders.append(getNewDDIGender(gender)));
}

function getNewDDIGender(val) {
  let $newDDI = $("<a>", {"class": "dropdown-item", href: "#", text: val});
  $newDDI.click((e) => {
    e.preventDefault();
    postGender(val);
    reloadFilters();
  });
  return $newDDI;
}

const postGender = async (val) => {
  fetch('/updateGender', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

function processCandidate() {
  $("#formCandidate").submit((e) => {
    e.preventDefault();
    let candidate = $("#inputCandidate").val()
    postCandidate(candidate);
    reloadFilters();
  });
}

const postCandidate = async (val) => {
  fetch('/updateCandidate', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const renderUpdate = () => {
  $("#submitUpdate").click((e) => {
    e.preventDefault();
    clearResultsDisplay(true);
    renderCandidatesData();
  });
}

const renderHistory = async () => {
  const history = await fetch('/history')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));

  let $generateFilters = $("#generate-filters");

  let $titleDiv = $("<div>", {"class": "col-md-1"});
  let $title = $("<p>", {text: "Filtros: "});
  $titleDiv.append($title);
  $generateFilters.append($titleDiv);

  let $filtersDiv = $("<div>", {"class": "col-md-11 flexFilter"});
  history.forEach((description, ind) => $filtersDiv.append(getNewActionTag(description, ind)));
  $generateFilters.append($filtersDiv);
}

function getNewActionTag(description, ind) {
  let $newCol = $("<div>", {"class": "flexItem"});
  let $newIcon = $("<i>", {"class": "fa fa-window-close"});
  let $newLabel = $("<span>", {"class": "badge badge-primary", text: description + " "});
  $newLabel.append($newIcon);
  $newCol.append($newLabel);
  $newIcon.click((e) => {
    e.preventDefault();
    postDelAction(ind);
    reloadFilters();
    console.log(description.slice(0,7));
    if (description.slice(0,7) == "Incluir") clearPartiesInclQueue();
    if (description.slice(0,7) == "Excluir") clearPartiesExclQueue();
    console.log("Updating...");
  });
  return $newCol;
}

const postDelAction = async (ind) => {
  fetch('/delAction', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({ind})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const renderAmountResults = async () => {
  const amount = await fetch('/amount')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));

  let $generateAmount = $("#generate-amount");

  let $titleDiv = $("<div>", {"class": "col-md-2"});
  let $title = $("<p>", {text: "Cantidad de Resultados: "});
  $titleDiv.append($title);
  $generateAmount.append($titleDiv);

  let $amountDiv = $("<div>", {"class": "col-md-10"});
  let $amount = $("<p>", {text: amount.toString()});
  $amountDiv.append($amount);
  $generateAmount.append($amountDiv);
}

const renderCurrentPage = async () => {
  const currentPage = await fetch('/currentPage')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));

  const amount = await fetch('/amount')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));

  let $generateCurrentPage = $("#generate-currpage");

  let $titleDiv = $("<div>", {"class": "col-md-1"});
  let $title = $("<p>", {text: "Página: "});
  $titleDiv.append($title);
  $generateCurrentPage.append($titleDiv);

  let $currentPageDiv = $("<div>", {"class": "col-md-11"});
  let $currentPage = $("<p>", {text: currentPage.toString() + " de " + (Math.ceil(amount/5)).toString()});
  $currentPageDiv.append($currentPage);
  $generateCurrentPage.append($currentPageDiv);
}

const renderArrows = async () => {
  const currentPage = await fetch('/currentPage')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));

  const amount = await fetch('/amount')
    .then(res => res.json())
    .catch(error => console.log("ERROR"));

  let $generateArrows = $("#generate-arrows");
  if (currentPage > 1) $generateArrows.append(getNewArrow("fa-arrow-left"));
  if (currentPage < (Math.ceil(amount/5))) $generateArrows.append(getNewArrow("fa-arrow-right"));
}

function getNewArrow(icon) {
  let $newCol = $("<div>", {"class": "flexItem"});
  let $newIcon = $("<i>", {"class": "fa " + icon});
  let $newLabel = $("<span>", {"class": "badge badge-primary"});
  $newLabel.append($newIcon);
  $newCol.append($newLabel);
  $newIcon.click((e) => {
    e.preventDefault();
    (icon == "fa-arrow-left") ? postPageChange(-1) : postPageChange(1);
    clearResultsDisplay(false);
    renderCandidatesData();
    clearSaved();
    console.log("Updating...");
  });
  return $newCol;
}

const postPageChange = async (val) => {
  fetch('/pageChange', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const goToPageN = async (val) => {
  fetch('/goToPageN', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({val})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const renderSave = () => {
  let $container = $("#saveButtonContainer");
  let $button = $("<button>", {type: "submit", "class": "btn btn-primary", id: "submitSave", text: "Guardar"});
  $container.append($button);
  $($button).click(function(e) {
    e.preventDefault();
    postSaveCandidates(getSaved());
    clearSavedDisplay();
    renderSaved();
    clearCheckboxes();
  });
}

function clearCheckboxes() {
  $("#generate-here").children(".candidate").each(function() {
    console.log("Clearing checkboxes")
    let $candidate = $(this).find(".row").find(".form-check").find(".form-check-label").find(".form-check-input");
    $candidate.prop('checked', false);
  });
}

const postSaveCandidates = async (inds) => {
  fetch('/saveCandidates', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({inds})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}

const renderSaved = async () => {

  const savedCandidates = await fetch('/saved')
      .then(res => res.json())
      .catch(error => console.log("ERROR"));

  $('#generate-saved').html('');

  if (savedCandidates.length == 0) {
    $("#generate-saved").append($("<p>", {text: "Ningún candidato guardado!"}));
    return;
  }

  let $titleWrapper = $("<div>");
  let $titles = $("<div>", {"class": "row"});
  Object.keys(savedCandidates[0]).filter(key => key != "H-Link").forEach(key => $titles.append(getNewCol(key.substring(2))));
  $titleWrapper.append($titles);
  let $titleHrTag = $("<hr>");
  $titleWrapper.append($titleHrTag);
  $("#generate-saved").append($titleWrapper);

  for (let i = 0; i < savedCandidates.length; i++) {
    let dict = savedCandidates[i]

    let $newWrapper = $("<div>");

    let $newRow = $("<div>", {"class": "row"});

    let $firstCol = $("<div>", {"class": "col-md-1"});
    let $firstTag = $("<a>", {href: dict["H-Link"], target: "_blank", text: dict["A-Nombre"]});
    $firstCol.append($firstTag);
    $newRow.append($firstCol);
    Object.keys(dict).slice(1).filter(key => key != "H-Link").forEach(key => $newRow.append(getNewCol(dict[key])));

    $newRow.append(renderDelButton(i));

    $newWrapper.append($newRow);

    let $newHrTag = $("<hr>");
    $newWrapper.append($newHrTag);

    $("#generate-saved").append($newWrapper);
  }
  clearSaved();
}

const renderDelButton = (ind) => {
  let $container = $("<div>", {"class": "col-md-1"});
  let $span = $("<span>");
  let $icon = $("<i>", {"class": "fa fa-window-close"});
  $icon.click((e) => {
    postDelCandidate(ind);
    clearSavedDisplay();
    renderSaved();
  });
  $span.append($icon);
  $container.append($span);
  return $container;
}

const postDelCandidate = async (ind) => {
  fetch('/delCandidate', {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify({ind})
  }).then(function (response) { // At this point, Flask has printed our JSON
      return response.text();
  }).then(function (text) {

  console.log('POST response: ');
  console.log(text);
  });
}
