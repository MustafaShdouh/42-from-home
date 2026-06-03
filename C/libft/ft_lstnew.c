/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 18:52:14 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/13 01:48:20 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
#include "libft.h"
//#include <stdlib.h>

t_list	*ft_lstnew(void *content)
{
	t_list	*node;

	node = (t_list *)malloc(sizeof(t_list));
	if (!node)
		return (NULL);
	node->content = content;
	node->next = NULL;
	return (node);
}

/*int	main(void)
{
	int		val = 42;
	t_list	*node;

	node = ft_lstnew(&val);
	if (node)
	{
		printf("Content: %d\n", *(int *)(node->content));
		if (node->next == NULL)
			printf("Next: NULL (Correct)\n");
		else
			printf("Next: %p (Wrong!)\n", node->next);
		free(node);
	}
}*/