/* =====================================================================
   TODAY: a wall of identical phones. On the build step the wall dims and
   the buried alerts light up ("urgent things get buried").
   ===================================================================== */
(() => {
  const wall = document.querySelector('[data-wall]');
  if (!wall) return;
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  wall.innerHTML = Array.from({ length: 80 }, () =>
    `<i class="mp${rnd() < .12 ? ' alert' : ''}" style="--d:${Math.round(rnd() * 900)}ms"><b></b><s></s><s></s><s></s></i>`
  ).join('');
})();

// Boot: honour #N in the URL (1-based)
go.ran = false;
go(Math.max(0, (parseInt(location.hash.slice(1)) || 1) - 1));
