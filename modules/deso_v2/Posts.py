import requests
import json
from modules.deso_v2.Route import getRoute

class Posts:

    def getUserPosts(username = "", publicKey = "",  numToFetch = 10, mediaRequired = False, lastPostHash= "",readerPublicKey = "BC1YLianxEsskKYNyL959k6b6UPYtRXfZs4MF3GkbWofdoFQzZCkJRB"):
        payload = {"PublicKeyBase58Check":publicKey,
                    "Username":username,
                    "ReaderPublicKeyBase58Check":readerPublicKey,
                    "LastPostHashHex":lastPostHash,
                    "NumToFetch":numToFetch,
                    "MediaRequired":mediaRequired}
        ROUTE = getRoute()
        endpointURL = ROUTE + "get-posts-for-public-key"
        response = requests.post(endpointURL, json = payload)
        return response.json()

    def getPostsStateless(
        postHash = "", 
        readerPublicKeyBase58Check = "BC1YLianxEsskKYNyL959k6b6UPYtRXfZs4MF3GkbWofdoFQzZCkJRB",
        orderBy = "", 
        startTstampSecs = 0,
        postContent = "",
        numToFetch = 10, 
        fetchSubcomments = False, 
        getPostsForFollowFeed = False, 
        getPostsForGlobalWhitelist = False, 
        getPostsByDESO = False, 
        mediaRequired = False,
        postsByDESOMinutesLookback = 0,
        addGlobalFeedBool = False
    ):
        payload = {
            "PostHashHex" : postHash,
            "ReaderPublicKeyBase58Check" : readerPublicKeyBase58Check,
            "OrderBy" : orderBy,
            "StartTstampSecs" : startTstampSecs,
            "PostContent" : postContent,
            "NumToFetch" : numToFetch,
            "FetchSubcomments" : fetchSubcomments,
            "GetPostsForFollowFeed" : getPostsForFollowFeed,
            "GetPostsForGlobalWhitelist" : getPostsForGlobalWhitelist,
            "GetPostsByDESO" : getPostsByDESO,
            "MediaRequired" : mediaRequired,
            "PostsByDESOMinutesLookback" : postsByDESOMinutesLookback,
            "AddGlobalFeedBool" : addGlobalFeedBool
        }
        ROUTE = getRoute()
        endpointURL = ROUTE + "get-posts-stateless"
        response = requests.post(endpointURL, json = payload)
        return response.json()

    def getPostInfo(postHash, commentLimit = 20, fetchParents = False, commentOffset = 0, addGlobalFeedBool = False, readerPublicKey = "BC1YLianxEsskKYNyL959k6b6UPYtRXfZs4MF3GkbWofdoFQzZCkJRB"):
        payload = {"PostHashHex":postHash,
                "ReaderPublicKeyBase58Check":readerPublicKey,
                "FetchParents":fetchParents,
                "CommentOffset":commentOffset,
                "CommentLimit":commentLimit,
                "AddGlobalFeedBool":addGlobalFeedBool}
        ROUTE = getRoute()
        endpointURL = ROUTE + "get-single-post"
        response = requests.post(endpointURL, json = payload)
        return response.json()
            
    def getHiddenPosts(publicKey):
        '''to get all the deleted posts of a user
        API credits: @Kuririn (https://bitclout.com/u/kuririn)'''
        paylod = {"userParams":
                    {"queryParams":
                        {"length":0},
                        "headersParams":{"length":0},
                        "cookiesParams":{"length":0},
                        "bodyParams":{"0":publicKey,"length":1}
                    },    
                    "password":"",
                    "environment":"production",
                    "queryType":"RESTQuery",
                    "frontendVersion":"1",
                    "releaseVersion":None,"includeQueryExecutionMetadata":True}
        response = requests.post("https://apps.tryretool.com/api/public/8952bb20-817f-46f0-b28f-67569f4db682/query?queryName=getHiddenPosts", json= paylod)
        return response.json()
