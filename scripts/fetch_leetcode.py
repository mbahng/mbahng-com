import urllib.request
import json
import random
import time
import os

url = "https://leetcode.com/graphql"
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def make_request(query, variables):
    try:
        data = json.dumps({'query': query, 'variables': variables}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def get_medium_problems(limit=30):
    # Total medium ~1500. Random skip.
    skip = random.randint(0, 1000)
    print(f"Fetching {limit} medium problems skipping {skip}...")
    
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        questions: data {
          title
          titleSlug
          difficulty
        }
      }
    }
    """
    variables = {
        "categorySlug": "",
        "limit": limit,
        "skip": skip,
        "filters": {"difficulty": "MEDIUM"}
    }
    
    res = make_request(query, variables)
    if res and 'data' in res and 'problemsetQuestionList' in res['data']:
        return res['data']['problemsetQuestionList']['questions']
    return []

def get_problem_content(title_slug):
    query = """
    query questionContent($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        content
      }
    }
    """
    variables = {"titleSlug": title_slug}
    res = make_request(query, variables)
    if res and 'data' in res and res['data']['question']:
        return res['data']['question']['content']
    return None

def main():
    problems = get_medium_problems(limit=20) # Fetch 20 to be safe on time
    results = []
    
    print(f"Found {len(problems)} problems. Fetching details...")
    
    for p in problems:
        content = get_problem_content(p['titleSlug'])
        if content:
            results.append({
                'title': p['title'],
                'content': content,
                'source': 'LeetCode',
                'url': f"https://leetcode.com/problems/{p['titleSlug']}/"
            })
            time.sleep(0.5) # Be nice
            
    print(f"Successfully fetched {len(results)} problems.")
    
    # Determine project root (one level up from this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    output_file = os.path.join(project_root, 'assets/json/leetcode_problems.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
