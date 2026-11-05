"""
Gradient descent on a 2D L-smooth function, verifying the descent lemma:

    f(w - eta * grad f(w)) <= f(w) - eta * (1 - L*eta/2) * ||grad f(w)||^2

Test function (non-convex, L-smooth):
    f(x, y) = 0.5*x^2 + 5*y^2 + 2*sin(x)*sin(y)

Hessian = diag(1, 10) + 2 * [[-sin x sin y, cos x cos y], [cos x cos y, -sin x sin y]].
The second matrix has spectral norm <= 2 (eigenvalues are -sin x sin y +- cos x cos y,
each in [-1, 1]), so ||Hessian|| <= 10 + 2*1 = 12 =: L  (a valid upper bound).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

L = 12.0


def f(w):
    x, y = w
    return 0.5 * x**2 + 5 * y**2 + 2 * np.sin(x) * np.sin(y)


def grad(w):
    x, y = w
    return np.array([x + 2 * np.cos(x) * np.sin(y),
                     10 * y + 2 * np.sin(x) * np.cos(y)])


def gradient_descent(w0, eta, K):
    ws = [np.array(w0, dtype=float)]
    for _ in range(K):
        ws.append(ws[-1] - eta * grad(ws[-1]))
    return np.array(ws)


def run(eta, K, w0, fname, view=None, check_decrease=True):
    ws = gradient_descent(w0, eta, K)
    fs = np.array([f(w) for w in ws])
    gnorms = np.array([np.linalg.norm(grad(w)) for w in ws])

    # Descent lemma: f(w_{k+1}) <= f(w_k) - eta (1 - L eta / 2) ||grad f(w_k)||^2
    # (valid for ANY eta by L-smoothness; it only implies decrease when eta < 2/L)
    bound = fs[:-1] - eta * (1 - L * eta / 2) * gnorms[:-1] ** 2
    holds = fs[1:] <= bound + 1e-9 * np.maximum(1, np.abs(bound))
    decreased = fs[1:] <= fs[:-1]
    print(f"eta = {eta:.4f} (2/L = {2 / L:.4f}), K = {K}")
    print(f"  Descent lemma inequality holds at {holds.sum()}/{K} iterations")
    print(f"  f decreases at {decreased.sum()}/{K} iterations")
    print(f"  f(w_0) = {fs[0]:.4g}, f(w_T) = {fs[-1]:.4g}, final ||grad|| = {gnorms[-1]:.3e}")
    assert holds.all(), "Descent lemma violated!"
    if check_decrease:
        assert decreased.all(), "f failed to decrease!"

    fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))
    ax = axes[0]
    if view is None:
        pad = 1.0
        view = (min(ws[:, 0].min(), -1) - pad, ws[:, 0].max() + pad,
                min(ws[:, 1].min(), -1) - pad, ws[:, 1].max() + pad)
    xs = np.linspace(view[0], view[1], 300)
    ys = np.linspace(view[2], view[3], 300)
    X, Y = np.meshgrid(xs, ys)
    hm = ax.pcolormesh(X, Y, f([X, Y]), cmap="viridis", shading="auto")
    fig.colorbar(hm, ax=ax, label="$f(x,y)$")
    ax.plot(ws[:, 0], ws[:, 1], "-o", color="red", markersize=3, linewidth=1.2)
    ax.plot(*ws[0], "o", color="red", markersize=7, markeredgecolor="white")
    ax.set_xlim(view[0], view[1])
    ax.set_ylim(view[2], view[3])
    ax.set_title(f"Gradient descent trajectory ($\\eta = {eta:.3g}$)")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")

    ax = axes[1]
    ax.semilogy(gnorms, color="tab:blue")
    ax.set_title(r"$\|\nabla f(w_k)\|$")
    ax.set_xlabel("iteration $k$")
    ax.grid(alpha=0.3)

    ax = axes[2]
    ks = np.arange(K)
    ax.plot(ks, fs[:-1], ":", label=r"$f(w_k)$", color="gray")
    ax.plot(ks, fs[1:], label=r"$f(w_{k+1})$", color="tab:blue")
    ax.plot(ks, bound, "--", label=r"$f(w_k)-\eta(1-\frac{L\eta}{2})\|\nabla f(w_k)\|^2$",
            color="tab:orange")
    ax.set_yscale("log")
    ax.set_title("Descent lemma: actual $\\leq$ bound")
    ax.set_xlabel("iteration $k$")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", fname)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print("  Saved", os.path.normpath(out))
    return view


if __name__ == "__main__":
    w0 = [4.0, 2.5]
    # eta = 1/L < 2/L: descent guaranteed
    view = run(1.0 / L, 60, w0, "descent_lemma.png")
    # eta = 0.2 > 2/L = 1/6: the inequality still holds, but decrease is NOT guaranteed
    run(0.2, 30, w0, "descent_lemma_large_step.png", view=view, check_decrease=False)
