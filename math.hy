(import [pandas :as pd])
(import [numpy :as np])
(import math)

(setv dataset (pd.read_csv "./output.csv"))
(setv time (get dataset "time"))
(setv score (get dataset "score"))

(defn math_expectation[col]
    (/ (col.sum) (len col))
)

(defn square[num]
    (* num num)
)

(defn dispersion[col]
    ( - (math_expectation (col.map square) ) (math.pow (math_expectation col ) 2) )
)

(print "Math expectation on time:"
    (math_expectation time)
)

(print "Math expectation on time(from numpy):"
    (np.mean time)
)
(print "Dispersion on score:"
    (dispersion score)
)
(print "Dispersion on score(from numpy):"
    (np.var score)
)
