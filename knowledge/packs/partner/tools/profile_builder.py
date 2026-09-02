import json
import os
import argparse
from pathlib import Path

def build_profile(slug, name, gender, age, occupation, mbti, sign, love_language, attachment_style, base_dir):
    """Build and save the partner's core profile."""
    profile = {
        "name": name,
        "gender": gender,
        "age": age,
        "occupation": occupation,
        "mbti": mbti,
        "astrological_sign": sign,
        "love_language": love_language,
        "attachment_style": attachment_style
    }
    
    target_dir = Path(base_dir) / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    
    profile_path = target_dir / "profile.json"
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
        
    print(f"Profile for {name} saved to {profile_path}")
    return str(profile_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build partner profile")
    parser.add_argument("--slug", required=True, help="Partner slug (e.g., my-gf)")
    parser.add_argument("--name", required=True, help="Partner name")
    parser.add_argument("--gender", default="Unknown", help="Gender")
    parser.add_argument("--age", default="Unknown", help="Age")
    parser.add_argument("--occupation", default="Unknown", help="Occupation")
    parser.add_argument("--mbti", default="Unknown", help="MBTI type")
    parser.add_argument("--sign", default="Unknown", help="Astrological sign")
    parser.add_argument("--love-language", default="Unknown", help="Primary love language")
    parser.add_argument("--attachment-style", default="Unknown", help="Attachment style")
    parser.add_argument("--base-dir", default="./partners", help="Base directory for partner skills")
    
    args = parser.parse_args()
    build_profile(
        args.slug, args.name, args.gender, args.age, args.occupation, 
        args.mbti, args.sign, args.love_language, args.attachment_style, args.base_dir
    )
