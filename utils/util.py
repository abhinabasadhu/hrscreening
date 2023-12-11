
# job match
def job_match(job, candidate):
    """ method to calculate profile matches job prospect or not"""
    matched_skills = []
    matched_custom_skills = []
    skill_points = 0
    custom_skill_points = 0

    for job_skill in job["skill_requirements"]:
        if job_skill in candidate["skills"]:
            skill_points += 1
            matched_skills.append(job_skill)

    for custom_skill in job["custom_requirements"]:
        if custom_skill in candidate["skills"]:
            custom_skill_points += 1
            matched_custom_skills.append(custom_skill)

    avg_required_skills = round((len(job["skill_requirements"]) + len(job["custom_requirements"])) / 2)

    if avg_required_skills >= (skill_points + custom_skill_points):
        good_match = True
    else:
        good_match = False

    return {
        "skill_matched_points": skill_points,
        "custom_skill_match_points": custom_skill_points,
        "job_matched_skill": matched_skills,
        "job_matched_custom_skill": matched_custom_skills,
        "good_match": good_match
    }

#
# def cal_distance(job, candidate):
#     """ method to calculate the distance between candidate and job """
