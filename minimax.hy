(import [numpy :as np])
(import random)
(import node)
(import math)
(defn get_random_map_title[x y]
    (if (= x 0) (if (= y 2) (return 2)))
    (if (= x 3) (if (= y 2) (return 3)))
    (if (= x 4) (if (= y 4) (return 4)))
    (setv title_num (random.randint 0 10))
    (if (< title_num 8) (return 0))
    (return 1)
)
(setv moves [[0 1] [1 0] [-1 0] [0 -1]])
(setv map (lfor x (range 5) (lfor y (range 5) (get_random_map_title x y))))

(for [x map] (print x))

(defn evaluate[x y temp_score]
    (+ (math.sqrt (+ (math.pow (- 4 x) 2) (math.pow (- 4 y) 2))) temp_score)
)
(defn find_moves_from_tree[^"Node" n depth]
    (setv move_node [[n.x n.y]])
    (for [neighbor (n.get_neighbors)]
        (do
            (if (< (math.fabs (- (neighbor.get_score) (n.get_score))) 0.1)
            (do
                (setv neighbor_node (find_moves_from_tree neighbor (+ 1 depth)))
                (setv move_node (+ move_node neighbor_node))
                (break)
            )
            )
        )
    )
    (return move_node)
)
(defn generate_minimax_tree_recurs[^"Node" max_player ^"Node" min_player depth temp_score]
    (if (> depth 4)
        (do
            (max_player.set_score (evaluate max_player.x max_player.y temp_score))
            (return max_player))
    )
    (if (= (% depth 2) 0)
        (do
        (for [side moves]
            (do

            (setv x (+ max_player.x (get side 0)))
            (setv y (+ max_player.y (get side 1)))
            (if (or (< x 0) (< y 0) (>= x (len map))) (continue))
            (if (or (>= y (len (get map x))) (= (get (get map x) y) 1))
            (continue))
            (if (= [x y] [min_player.x min_player.y]) (setv temp_score (- temp_score 1000)))
            (if (= [x y] [4 4]) (setv temp_score (+ temp_score 1000)))
            (setv neighbor (generate_minimax_tree_recurs (node.Node x y) min_player (+ depth 1) temp_score))
            (min_player.add_neighbor neighbor)
            ))
        (return min_player)
        )

        (do
        (for [side moves]
            (do

            (setv x (+ min_player.x (get side 0)))
            (setv y (+ min_player.y (get side 1)))
            (if (or (< x 0) (< y 0) (>= x (len map) ))
            (continue))
            (if (or (>= y (len (get map x))) (= (get (get map x) y) 1))
            (continue))
            (if (= [x y] [max_player.x max_player.y]) (setv temp_score (- temp_score 1000)))
            (setv neighbor (generate_minimax_tree_recurs max_player (node.Node x y) (+ depth 1) temp_score))
            (max_player.add_neighbor neighbor)
            ))
        (return max_player)
        )

)
)

(setv tree (generate_minimax_tree_recurs (node.Node 0 2) (node.Node 3 2) 0 0))
(print (find_moves_from_tree tree 0))