"""Build an auditable calibration dataset from locked predictions and outcomes."""
def build_rows(predictions, outcomes):
    outcomes_by=(lambda o:(o.get("candidate_anonymous_id"),o.get("choice_code")))
    index={outcomes_by(o):o for o in outcomes}
    rows=[]
    for p in predictions:
        if p.get("prediction_locked_before_result") is not True:
            raise ValueError("prediction must be locked before result")
        k=(p.get("candidate_anonymous_id"),p.get("choice_code"))
        o=index.get(k)
        if o is None:
            continue
        if p.get("admission_year")!=o.get("admission_year"):
            raise ValueError("admission year mismatch")
        rows.append({
            "candidate_anonymous_id":p["candidate_anonymous_id"],
            "admission_year":p["admission_year"],
            "quota_type":p.get("quota_type"),
            "region":p.get("region"),
            "choice_code":p.get("choice_code"),
            "selected_choice_order":p.get("selected_choice_order"),
            "predicted_probability":p["predicted_probability"],
            "accepted":1 if o.get("accepted") else 0
        })
    return rows
