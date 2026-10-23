import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")

from diferencial_evolution import de_rand_1_bin

FUNCOES = ["esfera", "ackley", "rastrigin"]
DIMENSOES = [2, 5, 10]
SEEDS = [101, 202, 303, 404, 505, 606, 707, 808, 909, 1010]
MAX_NFE = 20000
RHO = 100.0

F_BASE, CR_BASE = 0.5, 0.9

DIM_EXP, F_EXP = 10, 0.9

RHOS_ESTUDO = [1.0, 100.0, 1e4]
DIR_RESULTADO = "resultados"


def np_base(n):
    return max(10 * n, 20)


def rodar(funcao, n, NP=None, F=F_BASE, CR=CR_BASE, rho=RHO):
    NP = NP or np_base(n)
    runs = [
        de_rand_1_bin(funcao, n, NP, F, CR, rho, MAX_NFE, SEEDS[i])
        for i in range(len(SEEDS))
    ]
    print(
        f"{funcao:<10} n={n:<2} NP={NP:<3} F={F} CR={CR} rho={rho}"
        f"Viaveis = {sum(r['achou_viavel'] for r in runs)}/{len(runs)}"
    )
    return runs


def resumir(runs):
    r0 = runs[0]
    ok = [r for r in runs if r["achou_viavel"]]
    vals = np.array([r["melhor_f_viavel"] for r in ok])
    melhor = min(ok, key=lambda r: r["melhor_f_viavel"]) if ok else None
    return {
        "funcao": r0["funcao"],
        "n": r0["n"],
        "NP": r0["NP"],
        "F": r0["F"],
        "CR": r0["CR"],
        "rho": r0["rho"],
        "n_viaveis": len(ok),
        "taxa_sucesso": len(ok) / len(runs),
        "media": vals.mean() if ok else np.nan,
        "desvio": vals.std(ddof=1) if len(ok) > 1 else np.nan,
        "melhor_f": melhor["melhor_f_viavel"] if ok else np.nan,
        "melhor_x": melhor["melhor_x_viavel"].tolist() if ok else None,
        "nfe_medio": np.mean([r["nfe"] for r in runs]),
        "tempo_medio_s": np.mean([r["tempo"] for r in runs]),
        "frac_viavel_ini": np.mean([r["frac_viavel_ini"] for r in runs]),
    }


def convergencia(ax, grupos, titulo):
    for k, (rotulo, runs) in enumerate(grupos):
        H = np.maximum([r["hist"] for r in runs], 1e-12)
        cor = f"C{k}"
        ax.plot(H.T, color=cor, alpha=0.15, lw=0.7)
        ax.plot(np.median(H, axis=0), color=cor, lw=2, label=rotulo)
    ax.set(yscale="log", xlabel="NFE", ylabel="melhor valor penalizado", title=titulo)
    ax.grid(alpha=0.3, which="both")
    ax.legend()


def salvar(fig, nome):
    fig.tight_layout()
    fig.savefig(f"{DIR_RESULTADO}/{nome}.png", dpi=150)
    plt.close(fig)


def main():
    os.makedirs(DIR_RESULTADO, exist_ok=True)
    resumo, execucao = [], []

    def guardar(exp, runs):
        resumo.append({"experimento": exp, **resumir(runs)})
        execucao.extend(
            {
                "experimento": exp,
                **{k: v for k, v in r.items() if k != "hist"},
                "melhor_x_viavel": (
                    None
                    if r["melhor_x_viavel"] is None
                    else r["melhor_x_viavel"].tolist()
                ),
            }
            for r in runs
        )

    base = {}
    for f in FUNCOES:
        fig, axs = plt.subplots(1, len(DIMENSOES), figsize=(5 * len(DIMENSOES), 4))

        for ax, n in zip(axs, DIMENSOES):
            base[f, n] = rodar(f, n)
            guardar("principal", base[f, n])
            convergencia(ax, [("mediana", base[f, n])], f"{f}, n={n}")
        salvar(fig, f"convergencia_{f}")

    # 2) Parametro: Ackley, uma dimensao, so F muda (mesmas sementes e NFE)
    runs_f = rodar("ackley", DIM_EXP, F=F_EXP)
    guardar("param_base", base["ackley", DIM_EXP])
    guardar("param_variante", runs_f)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    convergencia(
        ax,
        [(f"F={F_BASE}", base["ackley", DIM_EXP]), (f"F={F_EXP}", runs_f)],
        f"Ackley n={DIM_EXP}: efeito de F",
    )
    salvar(fig, "experimento_parametro_ackley")

    # 3) Estudo de rho: Ackley n=10
    fig, ax = plt.subplots(figsize=(7, 4.5))
    grupos = []
    for rho in RHOS_ESTUDO:
        runs = rodar("ackley", DIM_EXP, rho=rho)
        guardar("estudo_rho", runs)
        grupos.append((f"rho={rho:g}", runs))
    convergencia(ax, grupos, f"Ackley n={DIM_EXP}: efeito de ρ")
    salvar(fig, "estudo_rho")

    pd.DataFrame(resumo).to_csv(f"{DIR_RESULTADO}/resumo.csv", index=False)
    pd.DataFrame(execucao).to_csv(f"{DIR_RESULTADO}/execucoes.csv", index=False)
    print(pd.DataFrame(resumo).drop(columns=["melhor_x"]).to_string(index=False))


if __name__ == "__main__":
    main()
