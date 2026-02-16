// Auth middleware removed — pass-through
function authMiddleware(req, _res, next) {
  req.user = { userId: "anonymous" };
  next();
}

module.exports = { authMiddleware };
