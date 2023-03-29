function formatToValidTuple(bbox){
  return [bbox._southWest.lat, bbox._southWest.lng, bbox._northEast.lat, bbox._northEast.lng];
}

export {
  formatToValidTuple
};
