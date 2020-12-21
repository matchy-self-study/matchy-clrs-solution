# 18.2 Basic operations on B-trees

## 18.2-1

Show the results of inserting the keys

```text
 F, S, Q, K, C, L, H, T, V, W, M, R, N, P, A, B, X, Y, D, Z, E
```

in order to an empty B-tree with **minimum degree 2**. Draw only the configurations of the tree just before some node must split, and also draw the final configuration.

### Answer

Insertion of `F`, `S` and `Q` will not make any node split.

Insertion of `K`:

```mermaid
flowchart LR
    subgraph A[Before K Insertion]
    root["fa:fa-circle"] --> node["F, Q, S"]
    end
    subgraph B[After Inserting K]
    root2[fa:fa-circle] --> node0["Q"]
    node0 --> node1["F, K"]
    node0 --> node2["S"]
    end
    A --> B
```

Insertion of `C` will not make any node split.

Insertion of `L`:

```mermaid
flowchart LR
    subgraph A[Before ]
    root2[fa:fa-circle] --> node0["Q"]
    node0 --> node1["C, F, K"]
    node0 --> node2["S"]
    end
    subgraph B
    root[fa:fa-circle] --> fq[F, Q]
    fq --> C
    fq --> n[K, L]
    fq --> S
    end
    A --> B
```

Insertion of `H`, `T`, `V` will not make any node split.

 W, M, R, N, P, A, B, X, Y, D, Z, E

Insertion of `W` and `M`:

 ```mermaid
flowchart TD
    subgraph A
    root[fa:fa-circle] --> fq[F, Q]
    fq --> C1[C]
    fq --> n[H, K, L]
    fq --> n2[S, T, V]
    end
    subgraph B
    root2[fa:fa-circle] --> fqt[F, Q, T]
    fqt --> C2[C]
    fqt --> hkl[H, K, L]
    fqt --> S
    fqt --> vw[V, W]
    end
    subgraph C
    root3[fa:fa-circle] --> Q
    Q --> fk[F, K]
    Q --> T
    fk --> C3[C]
    fk --> H
    fk --> lm[L, M]
    T --> S2[S]
    T --> vw2[V, W]
    end
    A --> B
    B --> C
 ```

 D, Z, E

```mermaid
flowchart TD
    subgraph A
    root3[fa:fa-circle] --> Q
    Q --> fk[F, K, M]
    Q --> T
    fk --> C3[A, B, C]
    fk --> H
    fk --> L
    fk --> np[N, P]
    T --> S2[R, S]
    T --> vw2[V, W, X]
    end
    subgraph B
    root[fa:fa-circle] --> q[Q]
    q --> fkm[F, K, M]
    q --> tw[T, W]
    fkm --> abc[A, B, C]
    fkm --> h[H]
    fkm --> l[L]
    fkm --> np2[N, P]
    tw --> S[R, S]
    tw --> v[V]
    tw --> xy[X, Y]
    end
    A --> B
```

```mermaid
flowchart TD
    subgraph B
    root[fa:fa-circle] --> q[K, Q]
    q --> fb[B, F]
    q --> M
    q --> tw[T, W]
    fb --> A
    fb --> cd[C, D]
    fb --> h[H]
    M --> l[L]
    M --> np2[N, P]
    tw --> S[R, S]
    tw --> v[V]
    tw --> xy[X, Y]
    end
```

```mermaid
graph TD
    root[fa:fa-circle] --> q[K, Q]
    q --> fb[B, F]
    q --> M
    q --> tw[T, W]
    fb --> A
    fb --> cd[C, D, E]
    fb --> h[H]
    M --> l[L]
    M --> np2[N, P]
    tw --> S[R, S]
    tw --> v[V]
    tw --> xy[X, Y, Z]
```
