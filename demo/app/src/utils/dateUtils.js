function formatToISOString(range){
  return `${range[0].toISOString()/range[1].toISOString()}`;
}

export {
  formatToISOString
};
